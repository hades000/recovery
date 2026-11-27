# RWB-P1-E1011-OPS Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1011-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P1-G |
| Ready to start | After RWB-P1-E1011-APP and RWB-P1-E1011-CON, with RWB-P1-E1015-APP and the RWB-P1-E1015-OPS base available |
| Size | Not specified in the source documents (DOR-RWB-P1-E1011-OPS-16); the squad sizes it at refinement |
| Depends on (build) | RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1015-APP, RWB-P1-E1015-OPS, RWB-PLT-E1071-CON |
| Contract dependencies | RWB-P1-E1011-CON, RWB-P1-E1015-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-case dated inputs (GAP-3273, GAP-3411) |
| Contract version | API Specification v7 `rwb-source-data.yaml` 5.1.0 (RD-P1-005); result-read fake 5.1.0; Temporal contract jar major 1 |
| Integration dependencies | AD018 job reads and failed-run rerun verification starting in wave 4 (ASM-5710) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-008, FR-P1-010, FR-P1-018, FR-P1-019, FR-P1-020, FR-P1-021, FR-P1-022, FR-P1-023) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P1-E1011-OPS-14) |
| Readiness decisions | RD-P1-001, RD-P1-002, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-008, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-022, RD-P1-024, RD-P1-025, RD-P1-028, RD-P1-040, RD-P1-042, RD-P1-043, RD-P1-044, RD-P1-045, RD-P1-065 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-011 for rwb-source-data. The reconciliation deploys as one api and one Temporal worker on task queue `rwb-source-data` in namespace `rwb-recovery`, scaled by KEDA on backlog and started by `rwb.source-data.AceDataReady.v1` or by the rerun path (DP-10; Architecture v5 slides 15 and 44). The lake extract job, the 07:30 Power BI refresh and the shared Quartz scheduler are removed from the release (DP-17; GAP-0495; ASM-0687). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1011-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 45 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Version 3 changes**

- RD-P1-022/024/040/044 retain the E1015 child handoff and E1015-OPS base ownership (RWB-P1-E1011-OPS#1, #4–#5, #8–#9, #16–#17, #22).
- RD-P1-001/004/005/011/012/020 specify the pinned contracts, AD018 boundary and test fixtures (RWB-P1-E1011-OPS#2–#3, #18, #20, #23–#24).
- RD-P1-025/028/042/043/044/045 align environment values, flags, deployment checks, alerts and rollback (RWB-P1-E1011-OPS#6–#7, #10–#15, #19–#21).
- Finishing pass (RD-P1-065; requests W2-tests-1060, W3-messages-0036; test case backfill): the pre-wave-4 restart wording follows the rerun standard, and Test Cases v9 IDs and the current resilience standard are cited.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied RD-P1-001, RD-P1-002, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-008, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-022, RD-P1-024, RD-P1-025, RD-P1-028, RD-P1-040, RD-P1-042, RD-P1-043, RD-P1-044, RD-P1-045.

### 1. Story

As a **platform engineer (delivery role)**, I want **the reconciliation child registration, compatibility-safe index migration, release checks and Reconciliation break alert deployed on the shared P1 chart**, so that **the operator can verify the daily run and respond to a BREAK or failed workflow**.

### 2. Business rationale

JOB-04 runs as a Temporal child on the shared P1 worker. Deployment must prove the handoff from E1015, the dated result reads and the operational signals.

RWB-P1-E1015-OPS owns the shared Helm chart and worker infrastructure. This release adds the reconciliation capability and verifies its changes against that base (RD-P1-044).

### 3. Preconditions

- The service template, chart skeleton and pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace exist, and KEDA is installed on the cluster (RWB-PLT-WF, RWB-PLT-E1071-CON).
- E1015-APP owns the ALS stamp and ACE event writes. E1015-OPS owns the shared chart, API and worker Deployments, probes, Flyway job, login reference, KEDA scaler and common P1 alerts. RWB-PLT-N002-INF owns the topic and producer ACL. P1 has no consumer group on its own source-data topic.
- The platform error envelope and the message catalogue are in force, so an alert carries a message ID and its agreed text.
- DEV, SIT, UAT and PROD exist with the parameter scope of LOV-ENVIRONMENT. Each release check uses that environment and the planned release business date.
- RWB-P1-E1069-DB owns SELECT on all 30 `recovery.v_ace_*` views for P1. This delta adds no grant. The reconciliation reads its E1011-APP section 11 views, with the batch-status gate owned by E1015.
- The APP image, CON contract and E1015-OPS base precede completion of this delta.

### 4. Flow

1. Build and scan one image digest and chart version. Render the E1015-OPS base and the E1011 delta using `values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` and `values-prod.yaml`. Promote the pinned digest through DEV, SIT and UAT, then obtain release-manager approval for PROD and deploy it in the change window.
2. Run the existing P1 per-service Flyway sequence before route readiness. This release adds the E1011 index migration only.
3. Register `ReconciliationWorkflow` and `reconciliation` on the E1015 worker under the deployed build ID. Use the base Temporal-backlog KEDA range 0 to n and the base API's two replicas (Environment and Deployment Design v6).
4. E1015 starts the child after the ALS stamp. Compare the rendered charts and check that E1011 adds no Kafka consumer, retry topic, dead-letter topic, Schedule or replacement base infrastructure.
5. Validate the rwb-case parameters and reference lists by release environment and date. Use the P1 workload identity and authorised one-hop calls.
6. Verify the Reconciliation break alert and shared Failed workflow alert against the synthetic fixtures and operator runbook.
7. In the E1015 SIT smoke profile in Kubernetes namespace `rwb-recovery`, use synthetic date 2026-11-30, a COMPLETED ALS batch and pinned dependency fakes. Run the E1015 readiness chain, verify the child on the shared queue and exercise both result reads with the R grant. Detail evidence awaits GAP-3413.
8. From wave 4 verify the AD018 failed-run rerun. A repeated readiness call starts no second `ReconciliationWorkflow` run (RD-P1-065). Pending: how a failed run is recovered before wave 4, owner solution architect, tracked as GAP-3390.

### 5. Exception paths

| ID | Trigger | Outcome | Covered by |
|---|---|---|---|
| X1 | Migration fails | Block rollout before serving traffic | AC1 |
| X2 | API or worker fails its own startup check | Mark rollout failed and follow AC10 | AC1, AC10 |
| X3 | No worker poll or unexpected build ID during smoke | Fail the worker check | AC2, AC20 |
| X4 | Parent lacks expected child start | Fail the smoke test and identify E1015 | AC3, AC20 |
| X5 | AD018 rerun refused | Use the AD018 Problem mapping | AC4, AC15, AC16 |
| X6 | Tolerance BREAK | Raise MSG-P1-012 and the Reconciliation break alert | AC6 |
| X7 | ACE or rwb-case read exhausts activity retries | Workflow fails, no partial rows, shared Failed workflow alert | AC6, AC9 |
| X8 | Date-specific parameter or required LOV missing | Stop promotion and report key/list, date and environment | AC5 |
| X9 | Configured backlog limit crossed | Scale the shared worker with the base KEDA policy | AC2 |
| X10 | Reconciliation flag off | Suppress reconciliation work and expose flagged operations as 404 MSG-P4-003 per RD-P1-045 | AC17 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Validates a delta on the E1015 base after the E1011 image and contract are available |
| Negotiable | Replica counts, resource sizes, the scaling threshold and the alert windows are environment values |
| Valuable | Makes reconciliation deployment, dated results and failure recovery visible to operators |
| Estimable | One child registration and index migration on the base, the reconciliation alert, smoke tests and runbook |
| Small | Pending squad sizing |
| Testable | Chart diff, smoke run, alert fixtures, permission checks and rollback |

### 7. Acceptance criteria

```gherkin
Feature: Deploy reconciliation on the shared P1 chart

  Scenario: AC1 Four environment renders and rollout order
    Given the E1015 base and E1011 delta values for DEV, SIT, UAT and PROD
    When the pipeline renders each environment and runs the release
    Then it uses a pinned chart version and image digest, runs the index migration before API readiness, and requires the separate API and worker probe checks
    And a failed migration or rollout check stops promotion

  Scenario: AC2 Shared worker scales on Temporal backlog
    Given the base worker has a KEDA minimum of zero and an environment-configured maximum and trigger
    When the reconciliation backlog crosses that trigger and a worker is replaced during the smoke date
    Then the base scaler adds a worker according to the published values, the registered build ID polls rwb-source-data, and one open execution resumes from history
    And exact threshold, maximum and cooldown evidence is pending GAP-3421

  Scenario: AC3 E1015 child handoff and infrastructure boundary
    Given the E1015 base chart and a COMPLETED ALS stamp for 2026-11-30
    When the E1011 delta is deployed and the parent commits the stamp
    Then the shared worker runs ReconciliationWorkflow recon-2026-11-30 and activity reconciliation
    And the chart diff adds no independent deployment, scaler, consumer, retry topic, dead-letter topic or Schedule

  Scenario: AC4 AD018 failed-run binding after wave 4
    Given AD018 has a FAILED JOB-04 run for 2026-11-30 and ALS is COMPLETED
    When RW-PLATADM submits and repeats a bodyless rerun with the same canonical UUID Idempotency-Key
    Then both answers are the same 202 Job in PENDING and only one new recon-2026-11-30 execution starts
    And a FAILED run on an incomplete ALS date answers 409 MSG-P1-001

  Scenario: AC5 Catalog preflight
    Given the configured environment and the planned release business date
    When the workload identity reads recon.tolerance.pct, case.entry.dpd, caselist.allocation.wait.until, LOV-PRODUCT and LOV-REC-RESULT
    Then it receives the applicable version of each value/list and the release fails with key, date and environment if a required value is missing

  Scenario: AC6 Reconciliation alert and workflow failure
    Given a synthetic SSME count BREAK of 12 and 0.4134 percent, and another workflow that exhausts ACE read attempts
    When the operators verify the alert rules
    Then one Reconciliation break alert routes MSG-P1-012 for SSME to the data steward by next morning
    And the E1015 shared Failed workflow alert routes to the platform administrator within 5 minutes with MSG-P3-037 and the run diagnostics include MSG-GEN-006 for ACE database

  Scenario: AC7 Dashboard and artifact scope
    Given a synthetic date with eight aggregate rows, one orphan and measured run duration and queue values
    When operators open the dashboard and inspect the deployment diff
    Then the panels show the seeded result, orphan, duration and queue values and the chart contains no lake or extract resources

  Scenario: AC8 Deployment permissions
    Given the base chart and the E1011 index migration
    When deployment permissions and the rwb-source-data identity are checked
    Then only the migration identity runs DDL in rwb_source_data and the worker calls rwb-case through the mesh with a 2 s client timeout
    And a cross-schema write attempt is denied

  Scenario: AC9 Activity retry is independent of Kafka
    Given the parameter fake returns 503 for every read attempt
    When reconciliation retries at 1 s initial interval, coefficient 2 and ten maximum attempts
    Then the Temporal execution fails and writes no partial results, and the shared workflow failure alert is raised
    And E1011 has no Kafka retry or dead-letter action

  Scenario: AC10 Flag-first rollback
    Given the E1011 release fails checks with an open workflow and the index applied
    When the release owner disables the feature and restores the previous tag/chart only if the fault persists
    Then the previous image passes smoke against the expanded schema, the index remains applied, and the prior worker build ID can replay the open workflow

  Scenario: AC11 No local dead-letter path
    Given an unprocessable AceDataReady is published
    When the E1011 deployment inventory is inspected
    Then it has no subscription, retries, local dead-letter record or replay step for that event

  Scenario: AC12 Duplicate automatic start
    Given two system starts target the same open recon-2026-11-30 execution
    When Temporal applies USE_EXISTING
    Then one open child remains and no duplicate aggregate key is committed

  Scenario: AC13 Missing-run evidence
    Given the ALS stamp and a readable allocation dependency
    When the 07:15 allocation wait limit is reached
    Then the smoke run verifies child scheduling and a diagnostic identifies a missing child
    And a production missing-result alarm cutoff awaits GAP-3422

  Scenario: AC14 ACE view boundary
    Given the runtime login rwb_source_data
    When the permission test checks direct ACE public tables and attempts a write to an ACE view
    Then the database denies both and the release adds no grant

  Scenario: AC15 Rerun access after AD018
    Given AD018 is released
    When a caller without a token, a caller without Platform administration U and an authorised caller with an unknown run UUID each submit otherwise accepted reruns
    Then they receive Problems 401 MSG-P4-001, 403 MSG-P4-002 and 404 MSG-P4-003 respectively and no execution starts

  Scenario: AC16 Rerun conflict after AD018
    Given AD018 is released and a JOB-04 run is open
    When an authorised caller submits a new UUID key for that date and type
    Then AD018 returns 409 MSG-P1-011 and leaves one open execution

  Scenario: AC17 Reconciliation flag off
    Given rwb.source-data.daily-gate is off
    When the release smoke attempts reconciliation and reads its flagged routes
    Then the feature writes no dated results and the routes respond 404 MSG-P4-003

  Scenario: AC18 Telemetry minimisation
    Given a complete synthetic run
    When logs, workflow inputs, metric labels and alert payloads are scanned
    Then none contains account, customer or case identifiers

  Scenario: AC19 Production promotion
    Given the pinned digest passed UAT
    When the release manager approves PROD in its change window
    Then PROD deploys the same image digest with its own values and preflight checks

  Scenario: AC20 Dated SIT smoke
    Given the shared SIT smoke profile, a pinned fake stack and synthetic 2026-11-30 with ALS COMPLETED
    When readiness runs and the authorised caller reads the aggregate results
    Then the worker runs the registered child, the API probe is healthy and the result page returns 200 with aggregates for that date
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the `rwb_source_data` login and no other service's credential | DP-02; Arch v5 slides 11 and 29 |
| BR2 | The migration is a per-service Flyway sequence in schema `rwb_source_data` and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | E1011 and E1015 provision no consumer of the P1 source-data topic. E1015 owns the outbox writes and the platform owns the producer ACL. | RD-P1-003/040/044 |
| BR4 | `ReconciliationWorkflow` is a child of E1015 `AceIngestCheck`; this release registers no Schedule or Quartz job | RD-P1-022, RD-P1-024 |
| BR5 | No environment value is hard-coded: replica counts, resource sizes, the scaling threshold and the alert windows come from values files and parameters | DP-06; Template and Rules §R7.2 s17 |
| BR6 | An alert carries a message ID with its agreed text and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | AD018 owns the JOB-04 failed-run rerun from wave 4, including UUID Idempotency-Key and its Problem answers. | RD-P1-001/004/012/024 |
| BR8 | The service writes only schema `rwb_source_data` and reads no other service's tables | DP-01 |
| BR9 | No lake path exists in the release: no extract job, no lake target, no Power BI refresh (DP-17) | Arch v5 slides 2 and 37; DP-17 |

### 9. State transitions

| From | Event | To |
|---|---|---|
| Not deployed | Approved pinned image and chart | Deploying |
| Deploying | Migration, probes, worker verification and preflight pass | Ready |
| Ready | Approved promotion of new digest | Rolling |
| Rolling | New pods healthy and compatible worker registered | Ready |
| Deploying or Rolling | Migration, probe, worker, parameter or smoke check fails | Failed |
| Failed | Feature disabled, previous tag restored if required and smoke passes | Ready with previous compatible behavior |

RD-P1-045 requires flag first, forward-only database changes, retention of the previous Temporal build ID and no termination of open workflows.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns chart delta, environment configuration, promotion checks, registration, alert and runbook |
| Platform administrator | Owns the shared platform rollout controls and receives Failed workflow alerts |
| ACE database administrator | Manages ACE view grants. P1 migration identity runs DDL under the platform Flyway job |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Follows the runbook for migration, worker, input failure or reconciliation BREAK |
| RW-PLATADM | Uses AD018 to operate a run with Platform administration U, when available |

Delivery roles are project responsibilities. Runtime actions use the permissions in E1011-CON and AD018-CON. Release owners control the flag and promotion through the established platform release controls.

### 11. Data

| Item | Content | Source |
|---|---|---|
| Shared deployment | Pinned digest, chart version, two API replicas, worker range 0 to n, resources, probe settings, flags and backlog scaling | Environment and Deployment Design v6; E1015-OPS |
| Aggregate | `rwb_source_data.reconciliation_result`, REC-01 and REC-02 | DF-OPS-118 through DF-OPS-129 |
| REC-05 inputs | `interaction.person_key`, `interaction.contact_key`, `party_ext.person_key`, `contact_point_ext.(contact_type, contact_key)`, `account_ext.account_key`, `valuation_ext.valuation_key` and dated case keys through rwb-case | DF-INT-003, DF-INT-022, DF-EXT-001, DF-EXT-013, DF-EXT-014, DF-EXT-027, DF-EXT-036; E1011-APP |
| Job projection after wave 4 | `job_run` and `job_run_check` | DF-OPS-233 through DF-OPS-251; AD018 |
| Parameters | `recon.tolerance.pct`, `case.entry.dpd`, `caselist.allocation.wait.until` from rwb-case. `recon.allocation.poll.minutes` = 5 in environment values | RD-P1-028/040/042; ASM-5708 |
| Flags | `rwb.source-data.daily-gate` and Section B lifecycle per E1015 and RD-P1-043/045 | RD-P1-022/043/045 |
| Secrets | Platform-managed secret references for runtime and migration logins, Temporal mTLS and the managed workload identity | DP-02/DP-11; Security and Access Design v5 |

For the first deployment, leave `rwb.source-data.daily-gate` off until the release owner has approved activation and the Section B dependencies are ready (RD-P1-043/045). Enable the flag for isolated DEV and SIT fixture runs through platform release controls. Pending: exact scaler maximum/trigger/cooldown per environment, owner E1015-OPS platform deployment owner, tracked as GAP-3421. Pending: inherited probe paths and startup windows, owner E1015-OPS platform deployment owner, tracked as GAP-3423.

### 12. Contract

#### 12.1 REST operations provided

The API exposes the two reconciliation GET routes in E1011-CON on `/api/recovery/source-data/v1` with Platform administration R and the shared Problem mappings. AD018 publishes and deploys the job operations. Detail smoke evidence remains pending GAP-3413.

#### 12.2 REST operations consumed

- Pending: paged rwb-case open-case key read for the business date (including case-account and case-party keys), owner rwb-case service owner, tracked as GAP-3273.
- Pending: rwb-case allocation status and exclusion operations, including paths, payloads, paging and provider fakes, owner rwb-case service owner, tracked as GAP-0337 and GAP-3411. The contract also needs to define the dated open-case balances and eligible account set for REC-02.
- Use the rwb-case parameter and reference-data paths in E1011-CON. The runtime and preflight use the P1 workload identity, mesh mTLS, and service-to-service rights for the consumed operations. Restrict egress to the declared providers. Confirm pending parameter grant under GAP-3420.

#### 12.3 Events published

RWB-P1-E1015-APP publishes `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` via outbox on `rwb.source-data.events.v1`, with schemas in RWB-P1-E1015-CON. E1011-APP uses DP-03 for `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (RD-P1-008).

#### 12.4 Events consumed

E1011 consumes no events. `AceIngestCheck` starts the child in the ALS-stamp workflow task (RD-P1-040/044).

#### 12.5 Workflows and activities

`ReconciliationWorkflow` (`recon-{businessDate}`) registers one activity, `reconciliation`, on task queue `rwb-source-data` in namespace `rwb-recovery` (contract jar major 1). The child input is `{businessDate, startedBy}`. E1015 starts it with parent close policy ABANDON in the workflow task that commits the ALS stamp (source status COMPLETED), using USE_EXISTING and ALLOW_DUPLICATE. Before REC-01, use durable timers to poll the rwb-case allocation answer every `recon.allocation.poll.minutes` (5 in the values file, ASM-5708). Proceed at ALLOCATION_COMPLETE YES or the `caselist.allocation.wait.until` limit (07:15 Asia/Bangkok, rwb-case parameter) when the contract is readable. An unreadable answer blocks the checks and produces no result rows (RD-P1-042).

The activity retry policy is initial interval 1 s, coefficient 2, maximum 10 attempts (Error Handling and Resilience Standard v5). Each remote call is one hop with a 2 s caller timeout and a breaker per downstream. Pending: activity start-to-close budget for the whole reconciliation, owner solution architect, tracked as GAP-3414.

The E1015 worker registers the two types at the pinned release build ID and uses mTLS to the Temporal frontend.

#### 12.6 Schedules

None. The child starts through E1015’s ALS-stamp handoff. AD018 can rerun a failed JOB-04 execution after wave 4.

#### 12.7 Tables owned

This release adds only `ix_reconciliation_date` on `rwb_source_data.reconciliation_result(business_date, rec_code, product_group)`, in the migration built by E1011-APP. E1015-OPS runs it using the shared Flyway job and the platform migration identity. Pending: confirm the next free D-RCV-28 migration filename and migration-role reference, owner P1 database release owner, tracked as GAP-3424. Existing tables and the RD-P1-025 baseline stay in place.

#### 12.8 Contract fakes

Pin the E1011-CON WireMock fake to 5.1.0 and use the E1015 smoke profile in pipeline and SIT. Pin the RWB-P3-E1042-CON and RWB-P3-E1043-CON provider versions when published. Catalog preflight uses the release business date and the authorised workload identity. Parameter effective-date semantics and provider grant remain pending GAP-3420. Use a COMPLETED ALS fixture for 2026-11-30, four product groups, PASS and BREAK, missing parameter, dependency timeout/503, and bad ACE view fixture. Dated rwb-case case and allocation fixtures await GAP-3273 and GAP-3411. AD018 job fakes are used from wave 4. Fakes are test-only workloads.

#### 12.9 Call-type summary

| Call type | Deployment surface |
|---|---|
| REST | Two result reads; dated rwb-case inputs, parameters, LOVs and authorise |
| Kafka | E1015 producer and platform ACL already exist; E1011 adds no consumer resource |
| Temporal | `ReconciliationWorkflow` and `reconciliation` on the shared worker |
| File | None (DP-17) |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 applies to the shared worker’s E1011 child registration. DP-17 removes the extract and report refresh. The console route remains in the admin integration.

**Artefacts**

| Artefact | E1011 delta |
|---|---|
| Shared E1015 Helm chart and environment values | E1011 flags and child registration. Render and compare in DEV, SIT, UAT and PROD |
| Flyway | E1011 index through the base migration job |
| Dashboard | Result rows and variances by code and product; tolerance; REC-05 orphan count; execution duration; worker replicas and queue backlog |
| Alerts | E1011 Reconciliation break rule and shared E1015 Failed workflow coverage |
| Runbook | BREAK; exhausted read; missing child/late batch; unhealthy worker; migration or rollout failure |

**Probes.** Reuse the E1015-OPS per-deployment probes. API readiness depends on its migration and API readiness signals. Worker health verifies the worker process and registered build ID during smoke. A legitimately scaled-to-zero worker does not take the API out of service. Exact paths and windows are pending in section 11.

**Alert mapping**

| Alert | Condition | Recipient and response |
|---|---|---|
| Reconciliation break | A persisted REC-01 or REC-02 BREAK (RD-P1-042). Include date, product, variance and percent per E1011-APP message mapping | Data steward by next morning (Observability and Monitoring Design v5) |
| Failed workflow | Temporal execution FAILED on `rwb-source-data` after retry exhaustion; include MSG-GEN-006 diagnostics for unavailable input | Shared E1015/platform alert MSG-P3-037 to platform administrator within 5 minutes |
| Load late / Load failed / stale | Owned and routed by E1015-OPS | Existing P1 shared monitoring |

The shared P1 dashboard and platform monitoring own standard latency, error, outbox age and failed-workflow signals. Kafka consumer-lag and dead-letter panels belong to the actual consuming workload. Pending: alert metric selectors, ticket channel and operational thresholds, owner observability owner, tracked as GAP-3418 and GAP-3418. Pending: reconciliation completion target and missing-result alarm cutoff, owner solution architect with data steward, tracked as GAP-3422. The 07:15 time is the allocation wait limit, and 05:30 is E1015’s late-source alarm time.

**Rollback.** Switch the reconciliation feature off first. If the fault persists restore the previous image tag and chart. Leave the index in place and fix forward with the next Flyway migration. Keep the prior Temporal build ID and open run histories, then smoke the previous image against the migrated schema (RD-P1-045).

**Done when.** The four renders, preflights, migration, smoke, dashboard, alert and rollback checks in section 16 pass. Verify the AD018 routes after release.

### 14. Validation and messages

| Message | Operational use |
|---|---|
| MSG-P1-012 | Reconciliation break alert; placeholders from E1011-APP |
| MSG-P3-037 | Shared Failed workflow alert |
| MSG-GEN-006 | Run diagnostic identifying the unavailable ACE database or rwb-case dependency |
| MSG-P1-001 | E1015 gate HOLD and AD018 incomplete-date refusal |
| MSG-P4-001 / MSG-P4-002 / MSG-P4-003 | 401 missing credentials, 403 missing right or scope, or 404 absent resource/flagged route, per RD-P1-004 |

### 15. Screens and states

The operator sees pipeline and release state, the shared dashboard and the runbook. Aggregate results are PASS or BREAK. Temporal execution failure is reported separately from a reconciliation outcome.

### 16. Test cases

| TC reference | Covers | Data |
|---|---|---|
| TC-P1-E1011-OPS-02, TC-P1-E1011-OPS-04, TC-P1-E1011-OPS-14, TC-P1-E1011-OPS-21, TC-P1-E1011-OPS-23, TC-P1-E1011-OPS-24 | AC1, AC3, AC10, AC17, AC19, AC20 | Four environment renders, dated SIT smoke, flag off, pre-deploy migration, rollback with open history and PROD same digest |
| TC-P1-E1011-OPS-02, TC-P1-E1011-OPS-03, TC-P1-E1011-OPS-08, TC-P1-E1011-OPS-15, TC-P1-E1011-OPS-16 | AC2, AC7, AC11, AC12 | Shared backlog scaling, synthetic dashboard results, absence of event subscription and overlapping starts |
| TC-P1-E1011-OPS-06, TC-P1-E1011-OPS-12, TC-P1-E1011-OPS-13, TC-P1-E1011-OPS-18, TC-P1-E1011-OPS-22 | AC5, AC8, AC9, AC14, AC18 | Versioned catalog values, missing key, timed-out reads, permissions, no retries on Kafka and telemetry minimisation |
| TC-P1-E1011-OPS-07, TC-P1-E1011-OPS-17 | AC6, AC13 | SSME break of 12, failed ACE view path, incomplete allocation at 07:15 and missing child diagnosis |
| TC-P1-E1011-OPS-01, TC-P1-E1011-OPS-19, TC-P1-E1011-OPS-20 | AC4, AC15, AC16 | AD018 wave 4 failed run, replay, missing credentials, rejected role, missing UUID, open run and incomplete batch |

### 17. Guardrails

- Use environment values for operational settings and the rwb-case catalog for business parameters.
- Events, workflow inputs, logs, dashboard series, alert payloads and the runbook carry business dates, product group codes, counts, amounts and durations only, with no direct or indirect identifier of a person or a case. The product group is classed Confidential, Customer data (Data Classification v5, DF-CAS-003): it is carried as a code only, never as a customer value and never beside a direct identifier.
- The runtime has the P1 database login and approved workload identity. The Flyway job uses the migration identity.
- P1 reads only the ACE views for ACE data. The E1069-DB grant is inherited, unchanged by this release.
- No cross-schema read and no cross-schema key: the migration job touches schema `rwb_source_data` only (DP-01).
- E1015-OPS owns the shared chart, worker and KEDA. This delta declares no Kafka consumer or inbox object.
- No lake path: no extract job, no lake target and no report refresh in the release (DP-17).
- No secret is written into a values file, a chart template, a dashboard or the runbook; every secret comes from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-007 | Dated account and reference reconciliation | Child registration and result panels | TC-P1-E1011-OPS-01 to TC-P1-E1011-OPS-04, TC-P1-E1011-OPS-06 to TC-P1-E1011-OPS-08, TC-P1-E1011-OPS-12 to TC-P1-E1011-OPS-24 |
| REQ-RDF-008 | Expose reconciliation breaks and orphans | Reconciliation break alert, orphan panel and runbook | TC-P1-E1011-OPS-01 to TC-P1-E1011-OPS-04, TC-P1-E1011-OPS-06 to TC-P1-E1011-OPS-08, TC-P1-E1011-OPS-12 to TC-P1-E1011-OPS-24 |
| REQ-CWC-004 | Exclusion rules are data | Parameter preflight and rwb-case dependency check | TC-P1-E1011-OPS-01 to TC-P1-E1011-OPS-04, TC-P1-E1011-OPS-06 to TC-P1-E1011-OPS-08, TC-P1-E1011-OPS-12 to TC-P1-E1011-OPS-24 |
| ADR-023 | Observability per service | Dashboard, Reconciliation break and shared Failed workflow alerts | TC-P1-E1011-OPS-03, TC-P1-E1011-OPS-08, TC-P1-E1011-OPS-15, TC-P1-E1011-OPS-16 |

### 19. Out of scope

- The application code of the checks, the workflow, the activity and the read operations (RWB-P1-E1011-APP).
- The contract documents and the fakes as published artefacts (RWB-P1-E1011-CON); this story deploys the test copies only.
- The platform topic provisioning implementation, the Temporal cluster and KEDA itself (platform epics RWB-PLT-EVT and RWB-PLT-WF).
- Common cluster and scaler topology are E1015-OPS base responsibilities.
- AD018 owns the job routes and failed-run rerun. P3 owns the case-list deployment.
- The lake extract job, the Power BI data set and the 07:30 refresh, which the target removes (DP-17).
- The dashboards and alerts of the sibling slices RWB-P3-E1011-APP, RWB-S5-E1011-APP and RWB-P6-E1011-APP.


### Remaining delivery steps

- Size: pending refinement; owner squad.
- Epic design sign-off: pending; owner product owner.
- Contract marked Done and published: pending; owner contract owner.
- Fake published: pending; owner contract owner.
- Test data loaded in DEV: pending; owner data engineer.
