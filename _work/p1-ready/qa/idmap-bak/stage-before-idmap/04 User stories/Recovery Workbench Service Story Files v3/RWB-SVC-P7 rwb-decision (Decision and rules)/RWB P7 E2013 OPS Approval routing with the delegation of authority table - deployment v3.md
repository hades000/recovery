# RWB-P7-E2013-OPS Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2013-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Size | Not specified in the source documents (DOR-RWB-P7-E2013-OPS-16); the squad sizes the story at refinement |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P7-Y |
| Ready to start | Day 1 |
| Depends on (build) | None (the platform contracts of the DP table are delivery prerequisites of the service template, not per-story blockers: RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) |
| Contract dependencies | RWB-P7-E2013-CON (build status Not started, not Done); RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON (published contracts of other services) |
| Contract version | Not specified in the source documents (DOR-RWB-P7-E2013-OPS-23); the story names the /v1 path only |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-017, FR-P7-018, FR-P7-020, FR-P7-021, FR-P7-022, FR-P7-023, FR-P7-024, FR-P7-025, FR-P7-026, FR-P7-035) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004, RD-P1-012 |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-004: Align the Error and Message Standard v6 wording.
- Backfill the published Test Cases v9 cross-references.
- RD-P1-012: the story no longer reads or reruns anything through the rwb-source-data job operations; migration runs are not jobs of those operations and are read from `flyway_schema_history` of `rwb_decision` (DP-15) (finding #1).
- The job read and rerun operations of rwb-decision are pending (GAP-3271) (findings #2, #4).
- The job view fake and the empty source-data fake are removed; the rwb-access delegation read is listed as consumed; AC13 added (findings #3, #5, #6).

**Change log.** D-RCV-60, 22 November 2026: deployment side of RWB-E2-013 for rwb-decision: the pipeline and image, the configuration and the secrets, Flyway on start with the drift gate, the Temporal worker of the approval task queue and its Schedules, the delegation snapshot refresh, the dashboards and the alerts of pending approvals and escalation breaches, and the run book with its rollback. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 28 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer of the rwb-decision service**, I want **one pipeline that builds one image and deploys the API part and the worker part of the service, the configuration and every secret reference wired per environment, Flyway running on start behind the drift gate, the Temporal worker registered on task queue `rwb-decision` in namespace `rwb-recovery` with the service Schedules registered, the delegation snapshot refreshed when its version changes, the dashboards and alerts that show pending approvals and escalation breaches, and a run book with a tested rollback**, so that **the approval routing of this service can be deployed, observed, escalated and rolled back without a hand change to a schema, a secret value or a Schedule**.

### 2. Business rationale

The routing rules of this legacy key are only as good as the deployment that runs them. Architecture v5 slide 33 deploys every service as an API part and a worker part on the same task queue, so the approval clock and its escalation exist only when the worker is registered and polling; slide 29 puts Flyway in each service's own pipeline and schema; the Temporal design puts one task queue per service in namespace `rwb-recovery`; and ADR-023 makes observability per service, with the dashboards and the alerts owned by the service that produces the numbers. This story fixes the deployment side of the approval capability: the image and its pipeline, the configuration and the secret references, the migration and the drift gate, the worker and the Schedules, the delegation snapshot and its refresh, the four alerts that matter for an approval queue, and the run book and the rollback.

It supports REQ-APD-001, REQ-APD-007 and REQ-APD-010 on the deployment side, NFR-052 for the secret references and ADR-023 for the observability of the capability. It creates no business behaviour: the routing itself is RWB-P7-E2013-APP and the contract is RWB-P7-E2013-CON, and neither is changed here.

### 3. Preconditions

- The service template and the Helm chart deploy a service as an API deployment and a worker deployment on one task queue (RWB-PLT-TPL; Architecture v5 slide 33).
- The `rwb_decision` schema, its login, its grants and its history table are created by the ACE DB work (RWB-PLT-NF06-DB, DP-02, DP-15); the approval table and its indexes are the app story's migration.
- The migration account and the read-only drift account of the service are entries in the key store (NFR-052).
- The platform Temporal workflow kit, the namespace `rwb-recovery` and the worker registration contract are published (RWB-PLT-E1071-CON, and the deployment side RWB-PLT-E1071-OPS).
- The Flyway, drift-gate and job-run conventions of the platform are published (RWB-PLT-E1044-CON and RWB-PLT-E1044-OPS) and each run is recorded in the service's own `flyway_schema_history` and the pipeline log (DP-15). Pending: job read and rerun operations of rwb-decision, owner solution architect, tracked as GAP-3271.
- The observability conventions of the platform — metric names, log fields, trace propagation and the alert routing — are published (RWB-PLT-OBS).
- No build dependency: the story has no build dependency and is Day 1 by rule (Template and Rules §R5.7).
- No production data is used in any configuration, fixture or test: every example, user key and amount is synthetic.

### 4. Flow

1. Pipeline: build and test the service image once; the same digest is promoted to every environment.
2. Pipeline: run the drift gate before the deployment to SIT, UAT and PROD: apply the migrations of the service to a clean container and compare the object list with the target schema of `rwb_decision` through the read-only account.
3. Pipeline: stop the deployment when the gate finds a difference; report only in DEV.
4. Deployment: on start, Flyway reads its account from the key store, applies each pending migration in the `rwb_decision` sequence once and writes the checksum to the service's own history table; the second instance waits for the lock and finds nothing pending.
5. Deployment: the API part starts on the service port behind gateway-bff and answers the health and readiness probes; no approval call is served before the schema is up to date.
6. Deployment: the worker part connects to the Temporal namespace `rwb-recovery`, registers its workflows and activities on task queue `rwb-decision`, and the worker version is recorded so that a running approval keeps its own history.
7. Deployment: the Schedules of the service are registered through the platform kit; a Schedule already registered is reconciled and not duplicated, and the approval clock itself is a durable timer of `ApprovalWorkflow` and not a Schedule.
8. Deployment: the delegation snapshot of the running service is warmed from `GET /api/recovery/access/v1/doa-limits` before the readiness probe passes, and it is refreshed when `rwb.access.DoaLimitChanged.v1` arrives without a restart.
9. Deployment: the dashboards and the four alerts of section 15 are published with the service, and the alert routing names the on-call rotation of the service rather than a person.
10. Operation: the run book is published, and the rollback is tested: the previous image digest is redeployed, the forward-only schema rule is respected, and the running approvals resume on the worker version they started on.
11. Operation: a failed run or a breach is read on SCR-44 Interface and job monitor and on the service dashboard, and after a failed migration the fix is merged as a new version that the pipeline deploys; the rerun operation of a failed job run of this service is pending (GAP-3271).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The drift gate finds an object the migrations do not produce | The deployment stops before it starts and the object is named | MSG-P3-016 | AC3 |
| X2 | An applied migration file was edited | Flyway validation fails, the pod does not become ready and the deployment stops | MSG-P3-016 | AC3 |
| X3 | The migration account cannot be read from the key store | The pod does not start; the failure is logged without the secret | None | AC2 |
| X4 | The worker cannot register on `rwb-decision` | The readiness probe fails, the pod is not put in service, and the approval timer is not served | None | AC4 |
| X5 | A Schedule is already registered and differs | The registration is reconciled to the chart value and the difference is logged; no second Schedule is created | None | AC5 |
| X6 | The delegation read does not answer during the warm-up | The readiness probe fails and no approval is routed on an empty snapshot; the reason is logged | MSG-GEN-006 | AC6 |
| X7 | A DoA version changes while approvals are open | The snapshot is refreshed, the open approvals keep the version stamped on them, and the transfer is logged | None | AC6 |
| X8 | The rollback is attempted with a pending destructive migration | The rollback is refused and the run shows the reason; PROD runs forward only and a fix is a new version | MSG-P3-016 | AC8 |
| X9 | An alert threshold cannot be met because no metric is emitted | The alert stays silent and the dashboard gap is raised as a defect of this story, not of the app | None | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the template, the chart, the per-service schema and login, the Temporal kit, the Flyway conventions and the observability conventions |
| Negotiable | The alert thresholds and the Schedule window are settled with the platform team; the rules of the migration, the worker and the secret reference are fixed |
| Valuable | A deployment can never change a schema by hand, run an approval on unregistered workers or lose an escalation without an alert |
| Estimable | One pipeline stage, one chart value set, the start configuration, the worker and Schedule registration, one refresh path, four alerts, one run book and one rollback test |
| Small | Fits one sprint with its tests |
| Testable | Each criterion runs in a pipeline against containers, a two-instance environment and the Temporal namespace |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the approval routing capability

  Background:
    Given the service is rwb-decision with schema rwb_decision, login rwb_decision and task queue rwb-decision in namespace rwb-recovery
    Given the migration account and the read-only drift account are secret references in the key store
    Given no production data is used in any configuration, fixture or test

  Scenario: AC1 One image, two parts and two instances (new, D-RCV-60)
    Given the service image built by the pipeline on the release branch
    When the image is promoted to SIT
    Then the API part and the worker part are deployed from the same image digest
    Then both parts run the same version and the worker reports its version to the Temporal namespace
    Then a second instance of the API part starts and serves the approval reads with no restart of the first
    Then the image carries no configuration value and no credential

  Scenario: AC2 Configuration and secrets are references, not values (new, D-RCV-60)
    Given the chart values of the service in SIT, UAT and PROD
    When the configuration is reviewed against the secret store and the parameters
    Then every account, password, certificate and token is a secret reference and never a value in the chart, the image or a pipeline file
    Then the route parameters, the capability areas and the service levels of the approval routing are read at run time from rwb-case and not copied into a chart value
    Then the feature switch rwb.decision.approval-routing is a parameter per environment with its value recorded
    Then a scan of the chart, the pipeline files, the image layers and the log output finds no credential and no personal value

  Scenario: AC3 Flyway on start and the drift gate (new, D-RCV-60)
    Given the platform Flyway and drift-gate conventions of RWB-PLT-E1044-CON and RWB-PLT-E1044-OPS
    When the service starts in SIT with two pending migrations in rwb_decision
    Then both migrate in version order, the history records their checksums, and the second start applies nothing
    When a column is added by hand to rwb_decision and the pipeline runs before SIT, UAT and PROD
    Then the gate fails with MSG-P3-016, names the object and stops the deployment
    Then PROD refuses Flyway clean and any undo file, and no object changes
    Then each applied version has one row in flyway_schema_history of rwb_decision, and the pipeline log holds the run with status APPLIED or FAILED

  Scenario: AC4 The Temporal worker registers on rwb-decision (new, D-RCV-60)
    Given the platform workflow kit of RWB-PLT-E1071-CON and its deployment contract
    When the worker part starts in SIT
    Then it registers on task queue rwb-decision in namespace rwb-recovery and polls no other queue
    Then ApprovalWorkflow and its four activities are registered and the worker version is recorded
    Then the readiness probe passes only when the worker is registered, and an approval started before a restart resumes on its recorded version
    Then no Quartz table, no shared job table and no run record of the retired Quartz job set is read or written

  Scenario: AC5 The service Schedules are registered and reconciled (new, D-RCV-60)
    Given the two Schedules of the service, the hash-chain check at 02:00 and the rule promote at 00:01, as their own stories define them
    When the deployment registers them through the platform kit
    Then each Schedule is created once with its cron, its overlap policy and its catch-up policy taken from the chart
    When a Schedule already exists with a different cron
    Then the registration reconciles it to the chart value and logs the difference, and no second Schedule is created
    Then the deployment creates no Schedule for the approval clock, because the approval clock is a durable timer of ApprovalWorkflow

  Scenario: AC6 The delegation snapshot is warmed and refreshed (new, D-RCV-60)
    Given the delegation read of rwb-access on GET /api/recovery/access/v1/doa-limits
    When the service starts
    Then the snapshot of the version in force is loaded before the readiness probe passes, and a failed or slow read keeps the pod out of service with MSG-GEN-006 in the log
    When rwb.access.DoaLimitChanged.v1 arrives for a new version with its effective date
    Then the snapshot is refreshed without a restart and the next routing decision reads the new version
    Then an approval already open keeps the limit version stamped on it and the refresh is logged with both versions

  Scenario: AC7 The dashboards and the four alerts are published (new, D-RCV-60)
    Given the observability conventions of ADR-023 and RWB-PLT-OBS
    When the service dashboard and the alert rules are published with the release
    Then the dashboard shows the items waiting by decision and level, the age of the oldest item, the due time distribution, escalations in the period, held items with no limit and the failures of the decision record
    Then an alert fires when an item passes its due time with no outcome, when an escalation fires and the new approver acts on none of the escalated items inside the next service level, when a commit of an approval is refused by the record library and when the delegation snapshot is older than the version in force
    Then every alert names the service, the decision, the level and the age, carries no personal value, and routes to the on-call rotation and not to a person
    Then a log line of the service names the approval ID, the case ID and the decision code only

  Scenario: AC8 The run book and the rollback are tested (new, D-RCV-60)
    Given the run book of the capability and the release that carries it
    When the rollback is exercised in SIT
    Then the previous image digest is redeployed for both parts, the schema stays forward-only and no destructive migration is reversed
    Then the running approvals resume on the worker version they started on and no approval is lost or duplicated
    Then the run book names the four alerts, the four failure paths of the app story, the drift gate, the worker and Schedule checks and the escalation contacts by role
    Then a rollback with a pending destructive migration is refused with MSG-P3-016 and the run shows the reason

  Scenario: AC9 An activity retry and timeout follow the chart policy (new, D-RCV-60)
    Given the timeouts and retry policy of readDelegation, routeApproval, recordOutcome and escalateApproval in the chart
    When an activity attempt exceeds its timeout or fails
    Then the attempt is retried under the chart retry policy and no further attempt starts once the policy is exhausted
    Then the run shows the attempt count and no approval is lost or duplicated

  Scenario: AC10 A consumed call fails or does not answer (new, D-RCV-60)
    Given the delegation read of rwb-access on GET /api/recovery/access/v1/doa-limits and the snapshot in force
    When the refresh read fails or does not answer
    Then the version in force stays in use, the next routing decision reads that version and the failure is logged with MSG-GEN-006
    Then no approval is routed on a snapshot that was not read, and no approval is lost or duplicated

  Scenario: AC11 One schema and one login per service (new, D-RCV-60)
    Given the run and the pods of rwb-decision in SIT
    When the service connects to the database
    Then every connection uses the login of rwb-decision and the schema rwb_decision
    Then a connection attempt to any other schema is refused and no object outside rwb_decision changes

  Scenario: AC12 The events go through the outbox and inbox library (new, D-RCV-60)
    Given the two events published and the one event consumed by the approval routing
    When the deployment is checked in SIT
    Then the two events are written through the outbox library and the one event is read through the inbox library
    Then the deployment creates no topic and adds no event of its own

  Scenario: AC13 A migration run is read from rwb-decision's own history and no rwb-source-data job operation is called (new, D-RCV-60)
    Given a SIT deployment applied one pending migration to rwb_decision
    When the platform administrator follows the run book to read the run
    Then the run is read from flyway_schema_history of rwb_decision with its version and checksum, and from the pipeline log with its status
    Then no request of this story reaches /api/recovery/source-data/v1/admin/jobs
```

These twelve criteria are new for the deployment of this capability and test only the deployment artefacts: the pipeline, the image, the chart, the secret references, the migration and the gate, the worker and the Schedules, the snapshot, the dashboards and the run book. They restate no business outcome and copy no legacy criterion.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One image per release, deployed as an API part and a worker part on one task queue; the two parts run the same version | Architecture v5 slide 33; RWB-PLT-TPL |
| BR2 | One schema and one login per service: the run and the pods use the login of rwb-decision and touch no other schema | Architecture v5 slide 29; DP-01; DP-02 |
| BR3 | Flyway runs on service start in every environment, one run per service, forward only in PROD, with the drift gate before SIT, UAT and PROD | RWB-PLT-E1044-CON; RWB-PLT-E1044-OPS; DP-15; ADR-021 |
| BR4 | The worker registers on task queue `rwb-decision` in namespace `rwb-recovery` and polls no other queue | Temporal and Drools design slide 10 notes; DP-10; RWB-PLT-E1071-CON |
| BR5 | The approval clock is a durable timer of `ApprovalWorkflow`; the deployment registers no Schedule for it, and JOB-05 stays retired | Architecture v5 slides 42 and 44; DP-10 |
| BR6 | The four alert rules, the dashboard and the run book are part of the release and are reviewed with it | ADR-023; RWB-PLT-OBS |
| BR7 | Every account, certificate and token is a secret reference from the key store; no credential appears in a chart, an image, a pipeline file, a log or a prompt | NFR-052 |
| BR8 | The delegation snapshot is read from rwb-access on `GET /api/recovery/access/v1/doa-limits` and refreshed by `DoaLimitChanged`; the deployment never copies the table | DP-08; Architecture v5 slide 41 |
| BR9 | The route parameters, the areas and the service levels are read at run time from rwb-case and never copied into a chart value | DP-06; Template and Rules §R7.2 s17 |
| BR10 | The observability names, fields and alert routing follow the platform conventions; an alert names a role and a rotation, never a person | ADR-023; Template and Rules rule 4 |
| BR11 | The rollback redeploys the previous digest and never reverses a destructive migration; a fix is a new version | RWB-PLT-E1044-OPS BR4; ADR-021 |
| BR12 | The deployment publishes the two events and consumes the one event of the app story through the outbox and inbox library; it adds no topic and no event of its own | DP-09; RWB-P7-E2013-CON |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Pipeline starts | The drift gate passes, or the flag is off in DEV | Building |
| Building | Image built and scanned | No credential and no critical finding in the image | Migrating |
| Migrating | All pending versions applied | The history records every checksum and the pipeline log holds the run | Registering |
| Registering | The worker registers and the Schedules reconcile | The task queue is polled and the two Schedules match the chart | Warming |
| Warming | The delegation snapshot is loaded | The read answers the version in force | Ready |
| Ready | A new release is promoted | The chart and the image differ from the running release | Rolling out |
| Ready | The rollback is exercised | The previous digest is redeployed and no destructive migration is pending | Ready on the previous version |
| Ready | The drift gate fails before the next deployment | An object is not produced by the migrations | Deployment stopped |

The approval states of the capability — WAITING, HELD_NO_LIMIT, APPROVED, REFUSED and RETURNED, with the escalation as a counter — are the app story's and are not changed here; this table is the deployment state only.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Runs a deployment through the pipeline and, after a failed migration, deploys the fix as a new version; reads the migration record from `flyway_schema_history`; the job rerun operation is pending (GAP-3271) |
| RW-DATASTEW, data steward | Reads the runs and the schema record (Platform administration R) |
| RW-AUDIT, internal audit | Reads the runs, the Schedule registrations and the alert history (Platform administration R) |
| DevOps engineer of rwb-decision | Owns the pipeline stage, the chart values, the start configuration, the worker and Schedule registration, the snapshot path, the alert rules and the run book |
| Pipeline migration account of the service | Applies the migrations of rwb-decision with that service's login from the key store |
| Key store administrator | Owns the secret entries and their rotation; not a Workbench role |
| Platform workflow kit owner | Owns the namespace, the worker registration contract and the Schedule convention this story reuses |

The letters are read from the platform administration area of the permission matrix; this story grants no business right and changes no approval right.

### 11. Data

No business field is created or changed by this story. The deployment records one run per deployment in `flyway_schema_history` of `rwb_decision` and in the pipeline log: the service, the schema, the version, the checksum, the drift result, `startedAt`, `endedAt` and a status of APPLIED or FAILED. It reads the migration account and the read-only drift account from the key store, the object list of `rwb_decision` from `information_schema`, and the delegation snapshot from rwb-access on its contract.

| Field | Content |
|---|---|
| service | The service name |
| schema | `rwb_decision` |
| version | The release version |
| checksum | The migration checksum |
| drift result | The drift gate result |
| startedAt | The run start time |
| endedAt | The run end time |
| status | APPLIED or FAILED |

Field types and LDM entries for the job-run record: Not specified in the source documents (DOR-RWB-P7-E2013-OPS-7).

The approval table, its fields and its indexes are the app story's (DF-DEC-032 to DF-DEC-053) and are not restated here. The job-run record fields beyond the legacy `Job` shape, the alert thresholds and the snapshot refresh interval are Not specified in the source documents (GAP-1253; ASM-2217) and (GAP-1256; ASM-2220); the fields that `flyway_schema_history` and the pipeline log hold, one alert per condition with a threshold agreed at the release review, and a refresh on the event are used until the register closes the points. Open decisions DL34 (ASM-0193) and DL35 (ASM-0189, ASM-0377, ASM-2041, ASM-2051) stay open; each is carried with its assumption until the register closes it.

### 12. Contract

Workflow ID form and start rule of `ApprovalWorkflow`: Not specified in the source documents (DOR-RWB-P7-E2013-OPS-8); the deployment registers no Schedule for it (BR5).

#### 12.1 REST operations provided

None. The deployment provides no REST operation; the approval operations are the app story's and are declared in RWB-P7-E2013-CON.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/access/v1/doa-limits` | rwb-access | The delegation read of the warm-up and the refresh (AC6) |

No operation of rwb-source-data is consumed: its `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` list and rerun only its own runs, and a migration run is not a job of those operations (RD-P1-012). Pending: job read and rerun operations of rwb-decision, owner solution architect, tracked as GAP-3271.

#### 12.3 Events published

None. The deployment publishes no event; the two events of the capability are published by the application through the outbox (RWB-P7-E2013-CON 12.3).

#### 12.4 Events consumed

None by the deployment itself. The service consumes `rwb.access.DoaLimitChanged.v1` for the delegation refresh, and that consumer is the app story's (RWB-P7-E2013-APP 12.4); this story only proves that the refresh reaches the running pods without a restart.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| ApprovalWorkflow | Workflow, registered by the worker part | `rwb-decision` | The worker registers it and its version; an approval started before a restart resumes on its recorded version. The workflow itself is RWB-P7-E2013-APP's. Workflow ID form: Not specified in the source documents (CG-ALL-7180). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-7180) |
| readDelegation, routeApproval, recordOutcome, escalateApproval | Activities, registered by the worker part | `rwb-decision` | Registered with their timeouts and retry policy from the chart; the activities are the app story's |

This story registers what the app story builds and changes neither the workflow nor an activity.

#### 12.6 Schedules

| Name | Cron | Overlap policy | Deployment element |
|---|---|---|---|
| JOB-14 hash-chain check | 02:00 every day | SKIP | Registered once and reconciled to the chart; owned by RWB-P7-E1008-APP |
| JOB-20 rule promote | 00:01 every day | SKIP | Registered once and reconciled to the chart; owned by the rule-version story of this epic |

The approval clock is not in this table: it is the durable timer of `ApprovalWorkflow`, and JOB-05 is retired (DP-10, BR5). The two Schedules are registered through RWB-PLT-E1071-CON; no Quartz row and no shared job table is read.

#### 12.7 Tables owned

None. The deployment owns no business table and creates none: `approval`, `decision_log_entry` and the library objects belong to the app and log stories of this service. Flyway writes `flyway_schema_history` inside `rwb_decision`, and that history table is not a business table.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-access delegation fake | `GET /api/recovery/access/v1/doa-limits` answering `DOA-2026.11` with the L6, L5 and L4 rows, and `DOA-2027.01` after the event; a delayed answer beyond 2 s and an unavailable answer | The warm-up and refresh tests of AC6 |

The fakes are the ones published by their owners; the drift test of RWB-P7-E2013-CON fails a build in which a fake and the document disagree.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 consumed | The delegation read of rwb-access; no rwb-source-data operation |
| Kafka | None published by the deployment | The service's two published and one consumed event are the app story's |
| Temporal | 1 workflow and 4 activities registered | `ApprovalWorkflow` with `readDelegation`, `routeApproval`, `recordOutcome` and `escalateApproval` on task queue `rwb-decision` |
| File | None | No file element in the deployment; the migrations are read from the image |

### 13. Solution plan

**Deliverables.** The golden pipeline stage that builds one image and runs the drift gate before SIT, UAT and PROD; the chart values that set `RWB_SCHEMA=rwb_decision`, point the migration and drift accounts at their key-store references, set the Temporal namespace, the task queue and the worker version and carry the two Schedule definitions; the start configuration with `spring.flyway.clean-disabled=true`, the lock and the readiness gate; the delegation warm-up and its `DoaLimitChanged` refresh path; the dashboard and the four alert rules; the run book and the rollback test.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The pattern set is the one of the legacy key and is applied on the deployment side: DP-10 is the worker and the Schedules, DP-15 is the start migration and the gate, DP-19 is the route the probes and the dashboard read through. No pattern is claimed for DP-02, DP-04, DP-05, DP-12, DP-14, DP-16, DP-17, DP-18 or DP-20.

**Build steps**

1. Add the drift-gate stage to the golden pipeline for SIT, UAT and PROD and wire the flag so a difference stops the deployment; prove the DEV report-only path.
2. Set the chart values: `RWB_SCHEMA=rwb_decision`, the two key-store references, the Temporal namespace and task queue, the worker version, the two Schedule definitions and the feature switch.
3. Set the start configuration: validation on start, out-of-order off, clean disabled in every profile, the lock on, and the readiness gate behind the schema version.
4. Wire the delegation warm-up before readiness and the `DoaLimitChanged` refresh path; prove the refresh without a restart.
5. Register the worker and the two Schedules; prove the reconciliation of a Schedule whose cron changed and the absence of an approval Schedule.
6. Publish the dashboard and the four alert rules with their thresholds and the role-based routing.
7. Write the run book and exercise the rollback in SIT, including the refusal of a rollback with a pending destructive migration.
8. Prove the scan: no credential in a pipeline file, the chart, the image or a log, and no personal value in a metric label or a log line.

**Done when.** The eight test cases of section 16 pass in SIT, the gate stops a drifted SIT, UAT and PROD deployment and reports it in DEV, the worker registers on `rwb-decision` and an approval survives a restart, the two Schedules reconcile, the delegation snapshot refreshes without a restart, the four alerts fire in the seeded conditions, and the rollback returns both parts to the previous digest with no approval lost.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-016 | Drift found, checksum mismatch, a refused clean or undo, or a failed migration | Schema check failed in {schema}: {object}. The deployment was stopped. |
| MSG-GEN-006 | The delegation read does not answer during the warm-up | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | A role without Platform administration R reads the runs | You cannot {action} here. Your role does not include it. |

MSG-P3-016 is the message of the platform migration contract, carried unchanged and shown in the pipeline log and on SCR-44, not to business users. MSG-GEN-006 is the platform message of a consumed call that does not answer in time, shown in the warm-up log. Neither message is reworded here.

### 15. Screens and states

No new screen. SCR-44 Interface and job monitor, through a gateway-bff composite route that calls each owning service (DP-19; the rwb-decision read is pending, GAP-3271), shows one deployment and migration run per service, in state Running, Failed or Complete, with the service, the schema, the version, the checksum and the drift result, and the two Schedule registrations with their last run. The service dashboard of ADR-023 shows the approval numbers of AC7. The empty, loading, error and no access states of SCR-44 are Not specified in the source documents (CG-ALL-7184).

| Signal | What it shows | Alert |
|---|---|---|
| Items waiting | The items in WAITING and HELD_NO_LIMIT by decision and level, and the age of the oldest | An item passes its due time with no outcome |
| Escalations | The escalations in the period, their level and the time to the next outcome | An escalation fires and none of the escalated items is acted on inside the next service level |
| Record failures | The commits refused by the decision-record library | Any refusal above zero in five minutes |
| Delegation snapshot | The version loaded, its effective date and its age | The snapshot is older than the version in force |

The four rules name the service, the decision, the level and the age, carry no personal value, and route to the on-call rotation by role.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P7-E2013-OPS-01 | AC1, BR1 | Component | One image promoted to SIT, both parts on the same digest, a second API instance starting with no restart |
| TC-P7-E2013-OPS-02 | AC2, BR7, BR9 | NFR | Scan of the chart, the pipeline files, the image layers and the logs; no credential, no personal value; the parameters read at run time |
| TC-P7-E2013-OPS-03 | AC3, BR3, BR11 | End to end | Two pending migrations in rwb_decision; a hand-added column in SIT, UAT and PROD stops the deployment and reports in DEV; PROD refuses clean and undo; one `flyway_schema_history` row per applied version and the run in the pipeline log |
| TC-P7-E2013-OPS-04 | AC4, BR4 | Component | Worker start in SIT; registration on rwb-decision only; an approval started before a restart resumes on its version |
| TC-P7-E2013-OPS-05 | AC5, BR5 | Component | The two Schedules created once; a changed cron reconciled; no approval Schedule created |
| TC-P7-E2013-OPS-06 | AC6, BR8 | Integration | Warm-up from the delegation fake; `DoaLimitChanged` for DOA-2027.01; an open approval keeps DOA-2026.11; a failed read keeps the pod out of service |
| TC-P7-E2013-OPS-07 | AC7, BR6, BR10 | Component | Seeded conditions for the four alerts; the dashboard panels; a log line with an approval ID, a case ID and a decision code only |
| TC-P7-E2013-OPS-08 | AC8, BR11 | End to end | Rollback to the previous digest with an approval in flight; a rollback with a pending destructive migration is refused with MSG-P3-016 |
| TC-P7-E2013-OPS-09 | BR12, §12 | Contract | Each operation, event and activity of §12 checked against RWB-P7-E2013-CON; the two events published and the one event consumed through the outbox and inbox library |
| TC-P7-E2013-OPS-10 | AC9 | Component | Activity forced past its timeout and failing once in SIT; retry under the chart policy; attempt count shown; no duplicate outcome |
| TC-P7-E2013-OPS-11 | AC10, BR8 | Integration | Delegation fake fails and does not answer on refresh; version in force stays in use; failure logged with MSG-GEN-006 |
| TC-P7-E2013-OPS-12 | AC11, BR2 | Component | Service started in SIT under login rwb_decision; connection to another schema refused; no object outside rwb_decision changed |
| TC-P7-E2013-OPS-13 | AC12, BR12 | Component | Two events written through the outbox library and one event read through the inbox library in SIT; no topic created by the deployment |
| TC-P7-E2013-OPS-14 | AC13 | End to end | One migration run read from `flyway_schema_history`; an access-log check for rwb-source-data job calls |

These thirteen cases are new for the deployment of this capability; no legacy test case of RWB-E2-013 is copied here, and TC-E2-013-01 to TC-E2-013-16 stay with RWB-P7-E2013-APP.

### 17. Guardrails

- One schema and one login per service: the run and the pods use the login of rwb-decision and touch no other schema (DP-01, DP-02).
- No credential in a chart value, an image layer, a pipeline file, a log or a prompt; every account is a secret reference from the key store (NFR-052, BR7).
- No drift-gate bypass in SIT, UAT and PROD; only DEV reports a difference instead of blocking it.
- Forward only in PROD: no clean, no undo file, no hand change; a fix is a new version through the pipeline (BR3, BR11).
- The worker polls task queue `rwb-decision` only and never another service's queue (BR4).
- No Quartz table, no shared job table and no JOB-05 row is introduced; the approval clock stays a durable timer (BR5).
- The delegation snapshot is read on the rwb-access contract and never copied into a chart, a table or an image (BR8).
- The route parameters, areas and service levels are read at run time and never copied into a chart value (BR9).
- No business value in a migration, a configuration default or an alert threshold that the business owns; thresholds are agreed at the release review and held as configuration.
- No personal data in a metric label, a log line, a trace attribute or a fixture; the alert payload carries the service, the decision, the level and the age only.
- ACE data only through the P1 or P4 contract; this deployment reads no ACE view.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-APD-001 | Route to the approver the delegation table names | The delegation snapshot of AC6 and the worker of AC4 | TC-P7-E2013-OPS-04, TC-P7-E2013-OPS-06 |
| REQ-APD-007 | An unanswered approval escalates to the named role | The worker registration, the durable timer proof and the escalation alert of AC7 | TC-P7-E2013-OPS-04, TC-P7-E2013-OPS-07 |
| REQ-APD-010 | Open items keep the version they were decided under | The refresh of AC6 and the log line with both versions | TC-P7-E2013-OPS-06 |
| NFR-052 | Database and drift accounts held in the key store | The chart reads the accounts as secret references; the scan proves no credential | TC-P7-E2013-OPS-02 |
| ADR-021 | Per-service Flyway and migration ownership | One run per service, forward only in PROD, the lock and the run record | TC-P7-E2013-OPS-03, TC-P7-E2013-OPS-08 |
| ADR-023 | Observability per service | The dashboard and the four alerts of AC7 | TC-P7-E2013-OPS-07 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The worker of AC4 and the Schedules of AC5 | TC-P7-E2013-OPS-04, TC-P7-E2013-OPS-05 |
| DP-15 | Per-service Flyway sequence | The start migration and the drift gate of AC3 | TC-P7-E2013-OPS-03 |
| DP-10 | Temporal instead of Quartz | The worker, the Schedules and the absence of an approval Schedule | TC-P7-E2013-OPS-04, TC-P7-E2013-OPS-05 |
| DP-09 | Outbox and inbox library for the events | The two published events and the one consumed event | TC-P7-E2013-OPS-09 |

### 19. Out of scope

- The routing, the outcome checks, the escalation logic and the workflow code (RWB-P7-E2013-APP).
- The contract document, the property lists and the fakes as published artefacts (RWB-P7-E2013-CON).
- The creation of the `rwb_decision` schema, its login and its grants (RWB-PLT-NF06-DB and the per-service DB work).
- The Flyway module wiring and the platform drift gate itself (RWB-PLT-E1044-APP-2 and RWB-PLT-E1044-OPS); this story consumes them.
- The platform dashboards and alert conventions beyond the four rules of this capability (RWB-PLT-OBS).
- The two Schedules as designed (JOB-14 in RWB-P7-E1008-APP, JOB-20 in the rule-version story); this story registers and reconciles them.
- The delegation of authority table and its versions, owned by rwb-access (RWB-P4-E1037-CON).
- The approval screen SCR-10 and the decision screen SCR-11 (RWB-P7-E2013-APP, RWB-P7-E2014-APP and RWB-PLT-N001-CON).
- The data lake: there is none (DP-17, ADR-018), and the deployment declares no lake element.
- Deployment slots, release windows and the cutover plan (DL34, DL35 and the cutover work).

### Remaining delivery steps

- Epic design sign-off and size: Pending where not stated (squad and design authority).
- RWB-P7-E2013-CON Done and its fakes published (rwb-decision contract owner).
- Name the rwb-decision job read and rerun operations (solution architect; GAP-3271).
- TC-P7-E2013-OPS-03 text aligned and the AC13 row added in Test Cases v9 (QA).
