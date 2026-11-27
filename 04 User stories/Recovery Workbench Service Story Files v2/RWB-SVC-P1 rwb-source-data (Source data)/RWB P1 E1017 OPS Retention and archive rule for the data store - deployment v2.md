# RWB-P1-E1017-OPS Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1017-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P1-K |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E1017-OPS-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1017-CON (build status Not started); contract version Not specified in the source documents (DOR-RWB-P1-E1017-OPS-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-028) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-017 for rwb-source-data. The legacy Quartz trigger leaves this key (JOB-17 is the rwb-document Schedule of Architecture v5 slide 44), so this deployment registers no Schedule and instead mounts the write-once container, scales the Temporal worker and wires the three legacy alerts to the retention run. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1017-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 16 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the rwb-source-data api and worker deployed from the service template with their Helm chart and values, their per-service Flyway migration job, their readiness and liveness probes, the Temporal worker on task queue `rwb-source-data` with KEDA scaling on backlog, the write-once archive container mounted with the service's own credential, the configuration of the batch size, the archive container and the purge setting, the three legacy alerts mapped to the new signals, the retention-run dashboards, the runbook entries and the capacity note**, so that **the monthly retention action runs predictably in every environment, an operator can see and act on a failed or refused run without reading code, and no Schedule of rwb-document is duplicated in this service**.

### 2. Business rationale

The legacy story leans on a Quartz trigger, a shared schema and an archive container that an operator mounted by hand. In the target a service is a Helm release built by one pipeline, with its own schema, login, container credential and Temporal worker (DP-02, DP-10, DP-15), and the monthly Schedule that starts the retention belongs to rwb-document (Architecture v5 slides 16 and 44; ASM-0076). Deployment is therefore part of the capability: a worker that never polls the queue leaves a run waiting, a container credential outside the service's own secret leaves the run Failed with MSG-GEN-006 at 02:30 on a Sunday, and an alert that only fires on an exception does not catch a rule set that was refused in full. This story makes the retention action observable, repeatable and safe to rerun, so the app story can be proved in SIT and the on-call rota can operate it.

It also keeps the boundary honest at deployment time. The run writes the eight P1 tables and one container and touches nothing else: no Schedule of another service, no rule table, no case table. That is checked in the chart, in the provisioning step and in the smoke run, not only in review.

The ownership behind that check is the one point the sources disagree on: TSD P1 v3 T3.6 still defines `retention_rule` as a P1 table, while the Ownership Map rules retention to P5 and Architecture v5 slide 44 puts JOB-17 in rwb-document. The Ownership Map is applied, so this release provisions no rule table and registers no Schedule, and the conflict is recorded as (GAP-0488; ASM-0680).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the namespace `rwb-recovery` are available, with the task queue naming rule `rwb-<service>` (RWB-PLT-WF, RWB-PLT-E1071-CON).
- RWB-PLT-TE012-APP has delivered a write-once container per environment, with an immutability policy and a credential scope that can be granted to one service login.
- The platform secret store holds the service's login secret, the container credential and the Temporal mTLS material; no secret is written into a values file.
- The platform error envelope and the message catalogue are in force, so an alert can carry a message ID and the legacy text.
- The three environments DEV, SIT and UAT exist, and the platform administrator holds the topic and queue registration rights.
- No build dependency: this story is Day 1 by rule (Template and Rules section R5.7).
- The applied patterns also name RWB-PLT-E1027-CON (DP-03), RWB-PLT-E1043-CON (DP-07), RWB-PLT-E1071-CON (DP-10), RWB-PLT-E1044-CON (DP-15) and RWB-PLT-N001-CON (DP-19), the reference-data contract RWB-P3-E1043-CON (DP-07) and the P4 authorise contract (DP-11); the story builds against the published contracts and fakes from Day 1 (GAP-2429).
- The exact cluster topology, replica counts, resource sizes, probe timings and KEDA thresholds are Not specified in the source documents (GAP-0490; ASM-0682); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded.

### 4. Flow

1. The pipeline builds the service image, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one Helm chart version from the same commit.
2. The chart deploys the api and the worker with the service's own login, the migration job and both probes; the migration job runs the per-service Flyway sequence for `rwb_source_data`, including the purge-setting migration of the app story, before the deployment is marked ready.
3. The provisioning step registers the Temporal task queue `rwb-source-data` in namespace `rwb-recovery`, wires the worker build ID and confirms that no Schedule is created in this namespace by this release.
4. The container step mounts the write-once container and grants the service credential the write, list and read scope on the container, with the path prefix `retention/`; a smoke write and read-back of one synthetic object proves the mount.
5. The configuration step sets `rwb.source-data.retention.batch-size=5000`, `rwb.source-data.retention.archive-container` and the purge setting `rwb.retention.purge`, and keeps the feature flag `rwb.source-data.retention` off until P5's JOB-17 is registered in the environment.
6. The dashboards are published: runs started, completed and failed; rows selected, archived, deleted and kept on hold per table; run duration; container write failures; refused rule sets by check; held cases.
7. The alerts are wired to the three message IDs of section 14 and to their runbook entries.
8. A smoke step starts one run for a synthetic run date in a test namespace through `POST /retention-runs`, checks the run record, the archive object and the manifest, and confirms that the probes answer healthy afterwards.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1 |
| X2 | The readiness probe fails after the start-up window | The pod leaves the service and the pipeline marks the release failed | None | AC3 |
| X3 | The worker does not poll the queue | Readiness stays false; a run awaits its first activity and no archive is opened | None | AC4 |
| X4 | The container mount or the credential is wrong | The smoke write fails and the release fails; in a run the same condition ends Failed with no row deleted | MSG-GEN-006 | AC5 |
| X5 | A second start arrives while a run is active | `409`, the active run id and the alert counter; the on-call operator waits, never reruns | MSG-P2-006 | AC7 |
| X6 | A rule set is refused in full | The run fails at the validation check and the alert names the check; no row is read | MSG-P1-002 | AC7 |
| X7 | The run is complete and Compliance has not read it | The summary alert carries the counts and the held cases | MSG-P1-020 | AC7 |
| X8 | A Schedule appears in this namespace for a retention job | The release check fails: JOB-17 belongs to rwb-document | None | AC6 |
| X9 | The purge setting is missing from the transaction | The delete fails and the unit fails; the live rows stay, and a rerun repeats the unit | None | AC6 |

X1 to X3 and X5 are the deployment and operation paths of the action. X4, X6 and X9 are the run's own failures carried onto the release. X8 is the check that keeps the ownership split visible in the cluster.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform queue registration, the container of RWB-PLT-TE012-APP and the workflow kit; no application code is built here |
| Negotiable | Replica counts, resource sizes, KEDA thresholds and probe timings are environment values, not story decisions |
| Valuable | Makes the monthly retention action deployable, observable and repeatable, with the ownership split visible in the cluster |
| Estimable | One chart, one pipeline stage, one migration job, two probes, one queue registration, one container mount, three configuration keys, three alerts, five dashboard panels and six runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the queue is registered, no Schedule exists, the alerts fire on a synthetic metric |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-source-data retention action

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The Helm chart and values deploy the api and the worker (new, D-RCV-60)
    Given the rwb-source-data Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the api and the worker with the rwb-source-data login and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_source_data before the deployment is marked ready
    Then no replica count, resource size, probe timing or batch size is hard-coded in the template

  Scenario: AC2 The pipeline builds, tests and promotes one artefact (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it builds one image and one chart version from the same commit
    Then it runs the unit, component and contract tests and fails the build on a contract drift with RWB-P1-E1017-CON
    Then it scans the image and the dependencies and fails on a critical finding
    Then it promotes the same artefact through DEV, SIT and UAT without a rebuild

  Scenario: AC3 Readiness and liveness probes answer (new, D-RCV-60)
    Given a running rwb-source-data pod
    When the readiness probe is called before the migration job and the start-up window complete
    Then the pod is not marked ready
    When the readiness and liveness endpoints are called after start-up
    Then both answer healthy without a database write
    Then a failing container mount or a stopped worker is reported as not ready and never as live-and-broken

  Scenario: AC4 The Temporal worker polls rwb-source-data and KEDA scales it (new, D-RCV-60)
    Given the worker deployment of the release
    When it starts in namespace rwb-recovery
    Then it polls only the task queue rwb-source-data
    Then the worker registers RetentionRunWorkflow and its eight activities with the build ID of the release
    Then a synthetic backlog on the queue scales the worker up and a drained queue scales it back to the floor
    Then no Schedule is created by this release in the namespace

  Scenario: AC5 The write-once container is mounted with the service's own credential (new, D-RCV-60)
    Given the container delivered by RWB-PLT-TE012-APP and the credential in the platform secret store
    When the release mounts it and the smoke step writes one synthetic object under retention/ and reads it back
    Then the write succeeds under the prefix retention/ and nowhere else in the container
    Then the release fails when the credential is missing or has no write scope
    Then an overwrite of the synthetic object is refused by the container's immutability policy
    Then no container credential appears in a values file, a chart template or a log

  Scenario: AC6 The configuration keys and the purge setting are released as values (new, D-RCV-60)
    Given the deployed configuration of the release
    When it is read from the environment
    Then rwb.source-data.retention.batch-size is 5000
    Then rwb.source-data.retention.archive-container names the container of the environment and not a literal account key
    Then the purge setting is present and is set only inside the delete transaction by the service
    Then the feature flag rwb.source-data.retention is off until P5's JOB-17 is registered in that environment
    Then a DELETE outside the purge setting and any DELETE on decision_log_entry are still refused by the database

  Scenario: AC7 The three legacy alerts fire with the legacy text and one runbook entry each (new, D-RCV-60)
    Given the published alert rules and the runbook
    When a synthetic run is replayed with a completed run, an unreachable container and a second start during an active run
    Then the summary alert carries MSG-P1-020 with the counts and the held cases
    Then the container alert carries MSG-GEN-006 with the system name "Archive container" and does not page on the first occurrence
    Then the second start counts and the operator alert carries MSG-P2-006 with the job name
    Then every alert links one runbook entry with the check, the owner role and the recovery step
    Then no alert payload carries a personal data field

  Scenario: AC8 The retention dashboards, the capacity note and the runbook are in place (new, D-RCV-60)
    Given the published dashboard and the capacity note
    When a month of synthetic runs is replayed for the eight tables in scope
    Then the dashboard shows runs started, completed and failed, and the rows selected, archived, deleted and kept on hold per table
    Then it shows the run duration, the container write failures and the refused rule sets by check
    Then the capacity note sizes the archive by the row volume of the eight tables and the monthly run, and names the retention of the workflow history
    Then the runbook covers a refused rule set, an unreachable container, a failed delete, a duplicate start, a failed migration and a probe failure

  Scenario: AC9 The business rules BR1 to BR8 hold in the release (new, D-RCV-60)
    Given the release and the business rules in section 8
    When the release is built, deployed to SIT and checked against the database and the namespace
    Then only the rwb-source-data login and schema rwb_source_data are used (BR1, BR8)
    Then the migration is the per-service Flyway sequence and runs before the deployment is ready (BR2)
    Then no Schedule for JOB-17 exists in namespace rwb-recovery (BR3)
    Then the worker polls only the queue rwb-source-data in namespace rwb-recovery (BR4)
    Then the write-once container is written under retention/ only and its immutability policy is not bypassed (BR5)
    Then no environment value is hard-coded and the batch size and container name come from values files (BR6)
    Then every alert carries a message ID and the agreed text and links one runbook entry (BR7)

  Scenario: AC10 A retried or timed-out activity does not duplicate a delete (new, D-RCV-60)
    Given a RetentionRunWorkflow activity that fails or exceeds its timeout
    When the worker retries the activity
    Then the retry does not delete any row a previous attempt already deleted
    Then the retry limit and the timeout values are Not specified in the source documents (NEWAC-RWB-P1-E1017-OPS-AC10)
    Then the outcome of a delete that exhausts its retries is Not specified in the source documents (NEWAC-RWB-P1-E1017-OPS-AC10)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-source-data login and no other service's credential | DP-02; Architecture v5 slides 11 and 29 |
| BR2 | The migration is a per-service Flyway sequence in schema `rwb_source_data` and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | The retention Schedule JOB-17 is rwb-document's; this release registers no Schedule and fails a check that finds one for it in the namespace | Architecture v5 slide 44; ASM-0076; DP-10 |
| BR4 | The worker polls one queue, `rwb-source-data` in namespace `rwb-recovery`, and KEDA scales it on backlog | Architecture v5 slide 11; DP-10 |
| BR5 | The write-once container is written under `retention/` with the service's own credential, and its immutability policy is never bypassed | NFR-074; RWB-PLT-TE012-APP |
| BR6 | No environment value is hard-coded: replica counts, resource sizes, thresholds, the batch size and the container name come from values files and parameters | DP-06; Template and Rules section R7.2 section 17 |
| BR7 | An alert carries a message ID and the agreed text, and links one runbook entry | Template and Rules section R7.2 section 14 |
| BR8 | The service writes only schema `rwb_source_data` and one container prefix; it reads no other service's tables and mounts no other container | DP-01 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart, the migration job and the container smoke pass the pipeline | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version, the worker polls and both probes answer | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains | Ready |
| Ready | Migration job failed | The schema is not at the expected version | Failed |
| Ready | Container mount or credential lost | The next run fails at the archive write | Degraded, with MSG-GEN-006 |
| Failed or Degraded | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the queue registration, the container mount, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the queue registration and the Schedule registration rights; confirms that JOB-17 stays in rwb-document |
| ACE database administrator | Owns schema `rwb_source_data`, the login and its grants, and approves the migration job including the purge-setting change |
| Container owner (RWB-PLT-TE012-APP) | Owns the write-once container, its immutability policy and the credential scope granted to the service |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the runbook entries and opens an incident when the container condition or a refused rule set persists |
| RW-PLATADM | Reads and starts a retention run in the running service, not in the cluster |

The per-service login name used by the chart is Not specified in the source documents (GAP-0490; ASM-0682); the chart references "the rwb-source-data login (DP-02)" through a secret reference and never a literal name.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, api and worker replica counts, resource requests and limits, probe paths and timings, log level, feature switches, KEDA thresholds | BR6 |
| Schema | `rwb_source_data`, migrated by the per-service Flyway sequence; the eight tables in scope of the run plus `data_product`, `sys_objects` and `sys_fields`. The interaction ledger stays in this schema under the same rule version. P5 rwb-document owns `retention_rule`, `retention_action`, the load and the JOB-17 Schedule; this schema holds no rule table, and the service receives the rule version, the run date and the rules in the run request, validates them against its own tables and applies them to its eight tables | BR2, BR8 |
| Container | The write-once container of RWB-PLT-TE012-APP, prefix `retention/`, immutable once written, with a manifest of the row count and the SHA-256 per file; read back before any delete. The container account, credential scope, immutability policy and manifest schema are Not specified in the source documents (GAP-0490) and stay with RWB-PLT-TE012-APP | BR5 |
| Queue | Temporal task queue `rwb-source-data` in namespace `rwb-recovery` | BR4 |
| Schedule | None in this service; JOB-17 is rwb-document's | BR3 |
| Configuration keys | `rwb.source-data.retention.batch-size=5000`, `rwb.source-data.retention.archive-container`, `rwb.retention.purge` (transaction setting), feature flag `rwb.source-data.retention` | BR6 |
| Dashboard series | runs started, completed, failed; rows selected, archived, deleted, kept on hold per table; run duration; container write failures; refused rule sets by check; held cases | Not specified in the source documents (DOR-RWB-P1-E1017-OPS-7) |
| Runbook entries | refused rule set, unreachable container, failed delete, duplicate start, failed migration, probe failure | BR7 |
| Secrets | The rwb-source-data login secret, the container credential and the Temporal mTLS material, all from the platform secret store | BR1 |
| Retention-run API | POST /retention-runs and GET /retention-runs/{runId} on /api/recovery/source-data/v1. The request and answer fields are Not specified in the source documents (GAP-0489); the field detail sits in RWB-P1-E1017-CON | Not specified in the source documents (DOR-RWB-P1-E1017-OPS-7) |
| Decision record | Archive and purge records are written as decision log entries: the decision code, final call, action and outcome values and the payload placement are Not specified in the source documents (GAP-2426) | Not specified in the source documents (DOR-RWB-P1-E1017-OPS-7) |

The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class, the exact probe timings and the KEDA thresholds) is Not specified in the source documents (GAP-0490; ASM-0682); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded.

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the two retention-run operations of the contract baseline behind the service's own route: `POST /api/recovery/source-data/v1/retention-runs` and `GET /api/recovery/source-data/v1/retention-runs/{runId}`. Owner rwb-source-data (P1). The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Interface | Path | Owner | Deployment need |
|---|---|---|---|
| `CaseHoldQuery` | Published interface, no REST path | P3 rwb-case | The legal-hold answer at run time; one hop, 2 s budget (DP-11) |
| Container put and get | The write-once container of RWB-PLT-TE012-APP under `retention/` | RWB-PLT-TE012-APP | The archive and its manifest, and the read-back check |
| Reference-data client library | `/api/recovery/case/v1` reference data | P3 rwb-case | The values a rule set may use; loaded at start-up (DP-07); contract RWB-P3-E1043-CON |
| Authorise contract | Not specified in the source documents (GAP-2429) | P4 | The caller's right on the run surface (DP-11) |

#### 12.3 Events published

None. The topic `rwb.source-data.events.v1` is provisioned for the service by the platform for its other events (`AceDataReady`, `AceDataLate`, owned by RWB-P1-E1013-APP); this release publishes no message for the retention action and creates no topic of its own.

#### 12.4 Events consumed

None. The retention run is started by the rwb-document Schedule through the contract call, so no consumer group and no retry topic is created for this capability.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `RetentionRunWorkflow` | Workflow, one run per run date and rule version | `rwb-source-data` | Worker deployment with the build ID of the release |
| `validateRules`, `selectRows(page)`, `archiveTable`, `verifyManifest`, `deleteArchivedRows`, `recordRun` | Activities | `rwb-source-data` | Registered by the same worker; KEDA scales on queue backlog |
| `casesOnLegalHold`, `caseNumbers` | Activities wrapping the interface | `rwb-source-data` | Registered by the same worker; mTLS to the Temporal frontend |

#### 12.6 Schedules

None. JOB-17 (retention, monthly, first Sunday) is a Temporal Schedule of rwb-document on queue `rwb-document` (Architecture v5 slides 16 and 44; ASM-0076), and this release fails its own check if a Schedule for the retention action appears in a namespace it deploys.

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| `interaction`, `case_list_row`, `reconciliation_result`, `data_product_load`, `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | P1 (`rwb_source_data`) | Created by the per-service Flyway sequence; the purge-setting migration is the version that follows |
| `data_product`, `sys_objects`, `sys_fields` | P1 (`rwb_source_data`) | Created by the same sequence; read by the run's validation |
| `retention_rule`, `retention_action` | P5 (`rwb_document`) | Not created, not mounted and not read by this release |
| `decision_log_entry` | P7 (`rwb_decision`) | Not created and never touched; the database keeps its unconditional refusal |

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-case `CaseHoldQuery` fake | Runs in the pipeline and in the SIT smoke profile, so a release can prove a run without rwb-case |
| Write-once container stub (Azurite in the lower environments) | Proves the mount, the manifest and the write refusal path before the real container is granted |
| rwb-source-data retention-run fake of RWB-P1-E1017-CON | Lets the P5 side be tested against the deployed route in SIT |
| rwb-case reference-data fake of RWB-P3-E1043-CON | Lets the release load reference data at start-up without rwb-case (DP-07) |
| P4 authorise contract fake | Lets the run right be checked in the pipeline and SIT without the P4 service (DP-11) |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 interface consumed in the deployment path | The run start and the run record; the legal-hold answer; one hop, 2 s |
| Kafka | None for this capability | The topic exists for the service's other events; no message and no consumer group is added here |
| Temporal | 1 workflow, 8 activities, no Schedule | `RetentionRunWorkflow` on `rwb-source-data` in `rwb-recovery`; KEDA scaling on backlog |
| File | 1 container prefix | `retention/` in the write-once container, with a manifest and an immutability policy |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is used here in its second form only: the worker runs a workflow that another service's Schedule starts, and this release registers no Schedule of its own. DP-15 covers the migration job and the purge-setting version it must apply. DP-19 is declared for the administration surface that reads a run and is built by another story. The five platform build dependencies, the reference-data contract RWB-P3-E1043-CON and the DP-11 authorise contract are carried in sections 3, 12.2, 12.8 and 13 and not in the header dependency rows (GAP-2429).

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-source-data/` | Chart with the api and worker deployments, service, migration job, config map, secret references, probes, container volume and the KEDA scaler |
| `helm/rwb-source-data/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, feature switches, batch size, container name, KEDA thresholds |
| Pipeline stage | Build, unit, component and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Task queue `rwb-source-data` in namespace `rwb-recovery`; the topic is the platform's and is not recreated |
| Container step | Mount, credential scope on the `retention/` prefix, immutability check and the smoke write and read-back |
| Dashboards | Run counts, rows per table, run duration, container write failures, refused rule sets, held cases |
| Alerts | Three rules, each with a message ID and one runbook entry |
| Runbook | Six entries: refused rule set, unreachable container, failed delete, duplicate start, failed migration, probe failure |
| Capacity note | Archive volume of the eight tables per month, container growth, workflow history retention |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the Temporal worker has polled `rwb-source-data` and the container mount answers; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database or to the container.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_source_data` with the service login, as a pre-deploy job with a backoff limit, and applies the purge-setting migration of RWB-P1-E1017-APP; a failed job blocks the rollout and the release.

**Alert mapping carried over from the legacy story.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-020 | A retention run completes | Summary alert with the counts per product and table, the rule version and the held cases | Compliance mailbox and dashboard, no page |
| MSG-GEN-006 | The archive container is unavailable or refuses a write | Container alert with the system name and the run id | Platform on-call, ticket; page only when it persists past the retry window |
| MSG-P2-006 | A start is posted while a run for that date is active | Duplicate-start counter and operator alert with the job name | Platform on-call, no page on the first occurrence |
| MSG-P1-002 | A rule set is refused in full at a check | Refused-rule-set alert naming the check and the table | Business on-call and Compliance, page |
| MSG-P4-002 | A caller without the run right | Refused-call count on the dashboard | No page |

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the probes answer, the queue is registered and KEDA scales, the container mount and the smoke write pass, the three alerts fire on synthetic metrics, the runbook entries are reviewed by the on-call rota and the capacity note is accepted.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-020 | Retention run summary to Compliance | {count} rows of {product} were archived under rule {rule} version {version}. {held} cases on legal hold were kept. |
| MSG-GEN-006 | Archive container unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | A start while the run is active | {job} is already running. Wait for it to finish before you run it again. |
| MSG-P1-002 | A rule set refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P4-002 | A caller without the right on the run surface | You cannot {action} here. Your role does not include it. |

The texts are copied unchanged from the legacy story; the deployment adds the alert routing and the runbook link, never a new wording. Thai text follows decision DL10, which stays open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive.

### 15. Screens and states

The deployment serves the two contract operations and no screen of its own. The operator-facing surfaces of this story are the pipeline run view, the release view, the queue and scaler view, the dashboards and the runbook. Compliance reads a run in the running service through `GET /retention-runs/{runId}`, which the platform administration surface of another P1 story exposes, and the retention classes show on SCR-47 Personal data from Epic 8. The gateway-bff composite route (DP-19) is not on this path. Screen Specifications v1, section SCR-47, gives the states loading and list; the empty, error and no access states of SCR-47 are Not specified in the source documents (CG-ALL-2209; DOR-RWB-P1-E1017-OPS-10).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-017-01 | AC1, AC2 | NFR | The chart renders for DEV, SIT and UAT with pinned digest, the service login reference and the migration job; one commit yields one image and one chart |
| TC-E1-017-02 | AC2 | NFR | Two rule versions, "RET-2026.11" at 24 months and "RET-2027.01" at 36 months, released through values only, with no rebuild |
| TC-E1-017-03 | AC3 | NFR | The container smoke, a held case "RW-2024-000311" with 40 rows, and the MSG-P1-020 summary carrying counts and no personal data |
| TC-E1-017-04 | AC4 | NFR | A refused rule set with 0 months, and a rule naming `decision_log_entry`, raise MSG-P1-002 on the named check |
| TC-E1-017-05 | AC5, AC7 | NFR | A container that refuses writes raises MSG-GEN-006 with the system name "Archive container" and deletes no row |
| TC-E1-017-06 | AC6 | NFR | A second start for 2026-12-06 during an active run answers 409 and raises MSG-P2-006 |
| TC-E1-017-07 | AC7 | NFR | A row at exactly 24 months is reported as kept; the purge setting is absent and the delete is refused |
| TC-E1-017-08 | AC8 | NFR | A rule for `decision_log_entry` is refused; no Schedule exists in the namespace and the database refusal stands |
| TC-E1-017-09 | AC4, AC8 | NFR | A backlog on the queue scales the worker; the dashboard shows the run and the duplicate-start counter |
| TC-E1-017-10 | AC3, AC4 | NFR | A caller without the run right is counted with MSG-P4-002; readiness answers false before the migration and true after |
| TC-E1-017-11 | §12, §12.5 | NFR | The workflow and activities listed in §12.5 match the published contract; no operation or event is used that the contract does not publish |
| TC-E1-017-12 | §12.7 (ASM-3438) | NFR | Each table owned by this release in §12.7 is created by the per-service Flyway sequence; `retention_rule`, `retention_action` and `decision_log_entry` are not created, mounted, read or touched |
| TC-E1-017-13 | AC9, BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 | NFR | Not specified in the source documents (NEWAC-RWB-P1-E1017-OPS-AC9) |
| TC-E1-017-14 | AC10 | NFR | Not specified in the source documents (NEWAC-RWB-P1-E1017-OPS-AC10) |

The legacy test case IDs of RWB-E1-017 are kept in order and character for character; each one now covers the deployment or operational element that carries its behaviour, because the behaviour itself is built in RWB-P1-E1017-APP, the rule in RWB-P5-E1017-APP and the surface in RWB-P1-E1017-CON. The legacy level "System" and "Access" map to "NFR" at this release. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in a values file: the months, the tables, the age-basis fields and the end action are data in the run request, never a deployment value.
- No personal data in logs, dashboard series, alert payloads or the runbook: counts, table names, case numbers, run ids and hashes only.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: this release mounts no ACE object and reads no view.
- No cross-schema read and no cross-schema key: the migration job and the run touch only `rwb_source_data`, and the legal hold comes over the rwb-case interface.
- One login per service and one container credential per service; the chart carries secret references and no literal credential (DP-02).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed.
- The container is write-once: a wrong archive is a new object at a new run date, never an overwrite, and no operator is granted a bypass of the immutability policy.
- No Schedule is created for the retention action in a namespace this release owns: JOB-17 stays with rwb-document (ASM-0076).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-013 | Retention and archive rule by record class | Queue registration, configuration keys, run dashboard and the MSG-P1-020 summary | TC-E1-017-01, TC-E1-017-03 |
| NFR-031 | Personal data is kept no longer than its policy allows | Batch size, purge setting and the migration job that applies it | TC-E1-017-04, TC-E1-017-07 |
| NFR-072 | A case under legal hold keeps every row | The held-case panel and the summary alert | TC-E1-017-03 |
| NFR-074 | No row is removed before its archive copy is checked | Container mount, immutability policy and the MSG-GEN-006 alert | TC-E1-017-05 |
| ADR-023 | Observability per service | Dashboard, three alerts and the six runbook entries | TC-E1-017-09 |
| ASM-0076 | Retention is rwb-document's; P1 keeps the ledger | No-Schedule check in the release and the namespace confirmation | TC-E1-017-08 |

### 19. Out of scope

- The application code of the run, the selection, the archive writer, the manifest check and the delete (RWB-P1-E1017-APP).
- The contract documents, the schemas and the fakes as published artefacts (RWB-P1-E1017-CON); this story only deploys the test copies.
- The retention rule, the retention action table and the monthly Schedule JOB-17 (RWB-P5-E1017-APP).
- The platform Temporal cluster, the namespace and its quotas (platform epics RWB-PLT-WF and RWB-PLT-E1071-CON).
- The write-once container, its immutability policy and its account (RWB-PLT-TE012-APP).
- The exact cluster topology, node pools, replica counts, probe timings and KEDA thresholds (GAP-0490).
- The case legal hold and the holding logic (rwb-case, P3).
- The screen of SCR-47 Personal data and the platform administration surface that reads a run (Epic 8 and the P1 administration story).
- The cross-service proof of the run across P1, P3 and P5 (RWB-ITG-E1017-ITG).
