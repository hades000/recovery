# RWB-P1-E1017-OPS Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

### Version 3 changes

- RD-P1-044: RWB-P1-E1015-OPS owns the base chart, Deployments, probes, migration job and scaler; this story is the retention delta (findings #3, #4, #15, #16, #17).
- RD-P1-045 and RD-P1-048: forward-only rollback standard, flag off answers 404, no archive destruction (findings #2, #5, #6, #12, #13).
- RD-P1-047, RD-P1-048 and RD-P1-024 (X-01): the retention operations, the seven-table boundary and periods Pending with Compliance (findings #7 to #11, #14, #19).
- Criteria AC11 to AC18 added. Open: archive identity and container (finding #1), alert thresholds and routes, capacity inputs and migration name (findings #10, #11, #18), listed in section 20.
- Finishing pass (requests W2-tests-1066, W5-runtime-0072; test case backfill): every criterion cites its Test Cases v9 row.

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
| Readiness decisions | RD-P1-005; RD-P1-024; RD-P1-044; RD-P1-045; RD-P1-047; RD-P1-048 |
| Parallel lane | L-P1-K |
| Ready to start | After RWB-P1-E1015-OPS, RWB-P1-E1017-APP and RWB-P1-E1017-CON; archive identity input Pending under GAP-0490 |
| Size | Not specified in the source documents (DOR-RWB-P1-E1017-OPS-16) |
| Depends on (build) | RWB-P1-E1015-OPS, RWB-P1-E1017-APP, RWB-P1-E1017-CON |
| Contract dependencies | RWB-P1-E1017-CON; rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE012-APP; RWB-P3-E1021-CON; platform security identity/codec decision |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-028) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-017 for rwb-source-data. The legacy Quartz trigger leaves this key (JOB-17 is the rwb-document Schedule of Architecture v5 slide 44), so this deployment registers no Schedule and instead mounts the write-once container, scales the Temporal worker and wires the three legacy alerts to the retention run. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1017-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 16 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied RD-P1-005; RD-P1-024; RD-P1-044; RD-P1-045; RD-P1-047; RD-P1-048.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want the shared rwb-source-data deployment to include the P1 retention worker registration, values, forward-only migration, storage identity boundary, observability and runbook as a delta on the base release of RWB-P1-E1015-OPS, so the P1 action runs on `rwb-source-data` in namespace `rwb-recovery` with ARCHIVE limited to `interaction` and REVIEW limited to the six ruled tables. Retention periods remain Pending, owner Compliance, tracked as GAP-1029. The chart, storage identity grant, safe smoke procedure and alert routing have open delivery inputs listed in section 20.

### 2. Business rationale

The monthly retention Schedule JOB-17 belongs to rwb-document (ASM-0076). P1 deploys the REST start/read operations and the Temporal worker that executes `RetentionRunWorkflow`; it does not register a Schedule. P1 archives `interaction` after verification, lists six tables as REVIEW/LISTED with no archive or delete, and does not include `case_list_row` (RD-P1-047; RD-P1-048; RD-P1-024/X-01).

The period values remain Pending with Compliance under GAP-1029. The archive target identity/path and manifest are Pending under GAP-0490, so the deployment story does not name a container or credential that has not been authorized. The retention purge flag is a transaction-local database setting owned by `RetentionPurger`; it is never a chart value or database default.

### 3. Preconditions

- Base release: RWB-P1-E1015-OPS owns the rwb-source-data chart skeleton and values, the api and worker Deployments, probes, Flyway migration job, login secret reference and the KEDA ScaledObject on the `rwb-source-data` task-queue backlog. This story adds values keys only and redefines none of them; it owns the retention run worker registration and the archive access of the worker (RD-P1-044).
- `RWB-P1-E1017-APP` and `RWB-P1-E1017-CON` deliver the service behavior and the API/Temporal contract. Build depends on both.
- P1 uses API Specification v7, `rwb-source-data.yaml` 5.1.0, and the P3 contract dependency RWB-P3-E1021-CON for retention-exclusions and closure-dates.
- The environment design gives the API two replicas and a worker KEDA minimum of zero; CPU/memory requests, limits, thresholds and probe timings remain environment values (GAP-2013). The namespace detail remains under GAP-2010.
- The worker polls queue `rwb-source-data` in namespace `rwb-recovery`; the release creates no P1 retention Schedule. JOB-17 remains with rwb-document (ASM-0076).
- The archive is reached by the P1 workload identity, with no static key or credential. RWB-PLT-TE012-APP grants its write-once storage to rwb-document only, so the container, the role and the prefix scope for rwb-source-data are Pending, owner solution architect, GAP-0490.
- Compliance periods remain Pending under GAP-1029. The deployment supplies no default retention period.
- `rwb.retention.purge` is set only inside the P1 delete transaction. No chart, ConfigMap, database default or operator role sets it (RWB-P1-E1017-APP).
- Values exist for DEV, SIT, UAT and PROD. The flag `rwb.source-data.retention` is off in every environment at release; while it is off both retention operations answer 404 (RD-P1-045). Pending: production approval path and the order of switching the flag on relative to JOB-17, owner release manager with the platform architect, NEW-GAP-S5-12 and NEW-GAP-S5-3.

### 4. Flow

1. The shared pipeline builds one image and chart version from one commit, runs the template gates, signs the image and publishes its SBOM. Each gate blocks promotion on failure.
2. DEV, SIT, UAT and PROD values pin chart version and image digest. The API deployment has two replicas; the worker KEDA minimum is zero. Resource sizes and scaler thresholds are values, not hard-coded template values (GAP-2013).
3. The Flyway job of the base release runs the P1 sequence, including the expand-only purge-guard migration of this story, in schema `rwb_source_data` before new API pods become ready. Rollback follows section 13.
4. The probes are those of the base release. This story adds no archive check to API readiness: the container has its own health indicator and alert. Worker polling is not part of API readiness; at KEDA minimum zero there is no worker pod.
5. The worker of the base release polls `rwb-source-data` in `rwb-recovery`; this story registers `RetentionRunWorkflow` and its eight activities on it under a new worker build ID (Worker Versioning). The release adds no Schedule.
6. The service identity, P3 authorise calls, decision-record producer grant, Temporal payload codec key and archive workload identity are deployment inputs. The grant table is in section 10; the principals and the key reference remain Pending under GAP-2429, GAP-2430 and GAP-0490.
7. The chart sets `rwb.source-data.retention.batch-size=5000` and the environment's archive-container reference only after the container decision; its concrete value is Pending under GAP-0490. It never sets `rwb.retention.purge`.
8. Smoke. In DEV and SIT: switch the flag on, post as the rwb-document identity a rule set that selects only seeded synthetic rows, expect 202 and then status COMPLETED, and switch the flag off. Archive objects stay, because nothing destroys them. In UAT and PROD the smoke leaves the flag off and expects 404 with no run. A run needs the archive grant of GAP-0490 and the run record table (NEW-GAP-S5-8).
9. Dashboards show run status and per-table selected, archived, deleted, listed and held counts for the seven ruled tables. Alerts use the four message mappings in section 14 and link their runbooks; routing details remain Pending as listed there.
10. PROD promotion uses the same signed digest as UAT with the flag off. The approval path is Pending, NEW-GAP-S5-12.

### 5. Exception paths

| ID | Trigger | Deployment or run result | Message | Covered by |
|---|---|---|---|---|
| X1 | Migration job fails | New pods do not become ready; pipeline stops; previous tag remains available | None specified | AC1, AC10 |
| X2 | API readiness dependency fails | API pod is not ready; container failure is reported separately and does not remove healthy API pods | Pending exact platform alert mapping | AC3 |
| X3 | Worker does not poll the queue | Worker readiness is false when a worker replica exists; the run stays RUNNING until a worker takes it | Pending exact threshold and message | AC4 |
| X4 | Archive identity or container access is denied | Run fails with MSG-GEN-006 after acceptance; no unverified interaction row is deleted | MSG-GEN-006 | AC5, AC12 |
| X5 | New start arrives for a RUNNING or COMPLETED run date | API returns 409 MSG-P2-006; no second P1 workflow runs | MSG-P2-006 | AC7 |
| X6 | The rule set is refused in full | 422; the run does not start; the refusal is observable by message code | MSG-P1-002 | AC7 |
| X7 | A deployment gate fails | Promotion stops; the prior release remains | None specified | AC2 |
| X8 | A Schedule is found for retention on P1 queue | Release policy check fails; JOB-17 remains in rwb-document | None | AC9 |
| X9 | A release is rolled back | Flag off first; no reverse migration; the previous tag runs against the forward schema | None | AC10 |
| X10 | A delete activity fails after all retries | Rows of the unit stay; run FAILED; alert with the run ID | MSG-GEN-006 | AC15 |

Alert thresholds, routes and exact runbook owners remain Pending under NEW-GAP-S5-13. The deployment does not set or bypass the transaction-local purge guard.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Retention-specific chart additions use the shared template and published contracts |
| Negotiable | Environment sizing, alert routing, storage grant and smoke procedure remain assigned to their owners |
| Valuable | The P1 worker, API and migration can be deployed and operated under the ruled ownership boundary |
| Estimable | Pipeline values, migration job, separate API/worker health, queue scaler, storage identity, dashboards and runbook |
| Small | One service deployment delta; the base chart stays with its platform owner |
| Testable | Each acceptance criterion checks a rendered chart, gate, health signal, queue, permission, dashboard, alert or rollback |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-source-data retention action

  Scenario: AC1 Values and the forward migration deploy on the base release
    Given the base release of RWB-P1-E1015-OPS and retention values for DEV, SIT, UAT and PROD
    When each release is rendered and deployed
    Then the API has 2 replicas and the worker KEDA minimum is 0
    And chart version and image digest are pinned
    And the retention values add rwb.source-data.retention.batch-size 5000 and the flag rwb.source-data.retention with value off
    And the purge-guard migration runs before new API pods become ready
    TC: TC-P1-E1017-OPS-01

  Scenario: AC2 Template pipeline gates stop promotion
    Given a commit on the service line
    When the shared pipeline runs
    Then build, unit, contract, boundary, migration lint, image scan, secret scan and personal-data scan run
    And each seeded gate failure blocks promotion
    And the published image is signed and has an SBOM
    TC: TC-P1-E1017-OPS-02

  Scenario: AC3 The archive container is not part of API readiness
    Given ready API pods
    When the archive container is unavailable
    Then every API pod stays ready
    And the container health indicator reports the failure and raises the MSG-GEN-006 alert
    TC: TC-P1-E1017-OPS-03

  Scenario: AC4 The worker takes the retention run from zero replicas
    Given the worker at KEDA minimum 0 in namespace rwb-recovery and the flag on in SIT
    When a retention run is accepted
    Then KEDA scales a worker for the backlog on task queue rwb-source-data
    And the worker has RetentionRunWorkflow and the eight activities of section 12 registered
    And it returns to 0 replicas after the queue drains
    And this release creates no Schedule
    TC: TC-P1-E1017-OPS-04

  Scenario: AC5 The archive identity follows the approved grant
    Given the P1 workload identity and storage grant are published under GAP-0490
    When the worker writes and reads a synthetic interaction archive object
    Then access is limited to the approved prefix
    And overwrite is refused by the container policy
    And no static key or secret appears in chart values, templates or logs
    TC: TC-P1-E1017-OPS-05

  Scenario: AC6 The purge guard is transaction-local
    Given a fresh database session and the rendered chart configuration
    When configuration and database defaults are inspected
    Then no chart, ConfigMap, database default or operator role sets rwb.retention.purge
    And DELETE on interaction outside the RetentionPurger transaction is refused
    TC: TC-P1-E1017-OPS-06

  Scenario: AC7 Retention signals map to four message IDs
    Given synthetic signals for a completed run, a failed run on an unavailable container, a second start for a running date and a refused rule set
    When the alert rules are evaluated
    Then they map to MSG-P1-020, MSG-GEN-006, MSG-P2-006 and MSG-P1-002 respectively
    And each alert carries the run ID where a run exists, a runbook link and no personal data
    TC: TC-P1-E1017-OPS-07; the 15-minute delivery check waits for the routes of NEW-GAP-S5-13

  Scenario: AC8 Dashboards use the ruled seven-table scope
    Given a synthetic retention run
    When the dashboard reads the run
    Then it shows run status and selected, archived, deleted, listed and held counts for the seven ruled tables
    And it has a panel for run status, one for counts per table and one for container health
    TC: TC-P1-E1017-OPS-08

  Scenario: AC9 No P1 retention schedule or cross-schema access is deployed
    Given the release chart and worker identity
    When the namespace and database grants are inspected
    Then the worker polls only rwb-source-data in rwb-recovery
    And no retention Schedule is registered by this release
    And the service login has no grant to another service schema
    TC: TC-P1-E1017-OPS-13

  Scenario: AC10 Rollback follows the standard without reversing schema
    Given release N with the purge-guard migration is deployed
    When the release owner rolls back
    Then the flag is switched off first and, only if that does not cover the fault, release N-1 is redeployed
    And no down migration or U script runs, the schema is unchanged and release N-1 passes its smoke against it
    And DELETE on interaction outside the purge transaction remains refused
    And running workflows are not terminated
    TC: TC-P1-E1017-OPS-14

  Scenario: AC11 A failed migration blocks the rollout
    Given the migration job fails
    When the release is deployed
    Then the previous pods keep serving, no new pod becomes ready and the pipeline stops
    TC: TC-P1-E1017-OPS-15

  Scenario: AC12 Another service is refused on the archive
    Given the workload identity of another service
    When it reads or writes under the retention prefix granted to rwb-source-data
    Then the request is refused
    TC: TC-P1-E1017-OPS-16

  Scenario: AC13 Caller and callee policy
    Given the identities of section 10
    When the rwb-document identity calls POST and GET /retention-runs with the flag on
    Then both reach the service
    And an identity not listed is refused with 403 MSG-P4-002
    And the rwb-source-data identity reaches the two rwb-case reads and may write rwb.decision-record.v1
    TC: TC-P1-E1017-OPS-17

  Scenario: AC14 Smoke run in SIT and in PROD
    Given seeded synthetic rows and a rule set that selects only them
    When the SIT smoke runs with the flag on
    Then it answers 202, the run ends COMPLETED, only seeded rows are archived and deleted and the flag is switched off afterwards
    When the PROD smoke runs with the flag off
    Then the retention operations answer 404 and no run or archive object exists
    TC: TC-P1-E1017-OPS-18

  Scenario: AC15 A failed delete raises an alert
    Given deleteArchivedRows fails on all 10 attempts of the catalogue retry (1 s initial interval, back-off 2)
    When the run ends
    Then the rows of the unit are still in interaction and the run is FAILED
    And an MSG-GEN-006 alert names the run ID and links the failed-delete runbook entry
    TC: TC-P1-E1017-OPS-19

  Scenario: AC16 No personal data and encrypted history
    Given a smoke run
    When logs, metrics, alerts and workflow history are inspected
    Then none holds personal data in clear
    And history payloads are encrypted by the payload codec
    TC: TC-P1-E1017-OPS-20

  Scenario: AC17 Production promotion
    Given the artefact accepted in UAT
    When it is promoted to PROD
    Then the image digest is identical and the flag is off
    TC: TC-P1-E1017-OPS-21

  Scenario: AC18 The delta changes no base object
    Given the rendered chart of the base release and of this release
    When they are compared
    Then the only differences are the retention values keys, the worker registration, the archive access and the retention alerts and dashboard
    TC: TC-P1-E1017-OPS-22
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The deployment uses the rwb-source-data login and schema `rwb_source_data`; it does not mount another service's credentials | DP-02; Architecture v5 |
| BR2 | Flyway is per-service, forward-only and expand-only; rollback is flag off first and then the previous tag, never a reversed migration | RD-P1-045; DP-15 |
| BR3 | JOB-17 belongs to rwb-document; this release creates no P1 retention Schedule | RD-P1-047; ASM-0076 |
| BR4 | Worker polls queue `rwb-source-data` in namespace `rwb-recovery`; KEDA minimum is zero | Architecture/Environment Design v6 |
| BR5 | ARCHIVE applies only to interaction; six other ruled tables are REVIEW/LISTED with no archive/delete; periods Pending Compliance GAP-1029 | RD-P1-048 |
| BR6 | The archive location and identity grant are not deployed before their owner decision under GAP-0490 | GAP-0490 |
| BR7 | The purge setting is not a deployment value; RetentionPurger sets it only in its transaction | RWB-P1-E1017-APP |
| BR8 | Alerts carry a message ID and a runbook link; owner, threshold and route remain Pending where section 20 says so | NFR-067; NFR-068 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Signed chart published | Shared pipeline gates pass | Ready to deploy |
| Ready to deploy | Flyway completes | P1 schema is at the forward migration version | Deploying |
| Deploying | API and worker checks pass | API dependencies and worker health are checked separately | Ready |
| Ready | New signed chart promoted | Same digest is used for the target environment | Rolling |
| Rolling | New pods pass readiness | Previous ReplicaSet drains | Ready |
| Deploying | Migration or deployment fails | Schema is not reversed; previous chart tag is redeployed | Failed release / rollback |

### 10. Authority

| Identity or role | Deployment authority |
|---|---|
| RW-PLATADM | Operates the release and runbook according to the assigned platform rights |
| RW-COMPLY | Reads a run through GET; no start, no deployment right |
| rwb-source-data workload identity | Reads/writes only the approved P1 database and archive resources; exact grants Pending under GAP-0490 and GAP-2429 |
| rwb-document service identity | Calls P1 POST/GET retention operations; grant is defined by the API/authorise contracts |
| rwb-source-data workload identity, outbound | rwb-case `retention-exclusions` and `closure-dates`; rwb-access authorise; write `rwb.decision-record.v1`; its own database login; Temporal payload codec key |
| RWB-P3-E1021-CON | Owns the P3 retention-exclusions and closure-dates reads |
| Release manager | Production promotion approval owner; approval path Pending, NEW-GAP-S5-12 |
| Solution architect / platform security owner | Settles archive identity, payload codec and service-to-service grants (GAP-0490, GAP-2429, GAP-2430) |

No credential or key is stored in chart values, ConfigMaps or logs.

### 11. Data

| Item | Deployment handling |
|---|---|
| Schema | `rwb_source_data`; only the rwb-source-data login is used (DP-02) |
| Retention tables | Seven in scope: ARCHIVE `interaction`; REVIEW-only `party_ext`, `account_ext`, `contact_point_ext`, `valuation_ext`, `dp_treatment`, `dp_guarantee_claim`. `case_list_row` is excluded under RD-P1-024 (X-01). |
| P3 facts | Retention-exclusions and closure-dates are read through RWB-P3-E1021-CON, never through a database grant |
| P5 rules | Rule rows and periods arrive in P1 request; periods remain Pending, owner Compliance, GAP-1029 |
| Archive | Container identity, name, prefix, path and manifest are Pending under GAP-0490 |
| Configuration | `rwb.source-data.retention.batch-size=5000`; archive-container reference only after its value is approved; flag `rwb.source-data.retention`, off at release (switch-on order Pending, NEW-GAP-S5-3) |
| Purge setting | `rwb.retention.purge` is transaction-local in `RetentionPurger`; it is absent from values, ConfigMaps, database defaults and operator grants |
| Service identity | Workload identity and resource grants; exact principal/resource mapping Pending under GAP-0490 and GAP-2429 |
| Temporal | Task queue `rwb-source-data`; namespace `rwb-recovery`; payload codec key reference Pending under GAP-2430 |
| Decision record | rwb-source-data may write `rwb.decision-record.v1` (RD-P1-003); what a retention run writes there is Pending, GAP-2426 |
| Observability | Status and counts per table; exact metric names for dashboard, capacity and alerts Pending under NEW-GAP-S5-13 |

The run consumes only the seven-table boundary and uses ARCHIVE or REVIEW; it does not deploy a retention period or add a P1 retention Schedule.

### 12. Contract

| Surface | Owner | Deployment requirement |
|---|---|---|
| `POST /api/recovery/source-data/v1/retention-runs` | P1 | Publish API Specification v7 / `rwb-source-data.yaml` 5.1.0; rwb-document calls with UUID Idempotency-Key; 202 accepted, 409 conflicts, 422 refusal; 404 while the flag is off |
| `GET /api/recovery/source-data/v1/retention-runs/{runId}` | P1 | Read status/counts, archiveLocation and holdReport |
| `GET /api/recovery/case/v1/cases/retention-exclusions` | P3 | One-hop 2 s call; read at start and before each interaction delete unit |
| `GET /api/recovery/case/v1/cases/closure-dates` | P3 | One-hop 2 s call for interaction age basis |
| `RetentionRunWorkflow` | P1 | Worker polls queue `rwb-source-data`, namespace `rwb-recovery`, ID `retention-run-{runDate}` |
| `rwb.decision-record.v1` | P1 decision-record library | Producer ACL per RD-P1-003; record content Pending, GAP-2426; codec key GAP-2430 |
| Archive target | Platform storage | Container, workload identity and prefix scope Pending under GAP-0490 |

The P1 worker applies ARCHIVE only to `interaction`; the six other tables are REVIEW/LISTED only. JOB-17 and its Schedule remain with rwb-document (ASM-0076). The release must not grant access to a P3 or another service schema.

### 13. Solution plan

**Release scope.** A delta on the base release of RWB-P1-E1015-OPS: retention values keys, worker registration, the purge-guard migration, archive access, the container health indicator, retention alerts, dashboard and runbook entries. Replicas, probes, migration job and scaler are the base release's and are not redefined (RD-P1-044).

**Release steps**

1. Add the retention values keys for DEV, SIT, UAT and PROD; the chart version and image digest are pinned. The base release gives API replicas 2 and worker KEDA minimum 0; sizes and thresholds are values (GAP-2013).
2. Run the shared pipeline gates: build, unit, contract, boundary, migration lint, image scan, secret scan and personal-data scan. The image is signed with its SBOM; any failed gate blocks promotion.
3. Ship the expand-only purge-guard migration as `V<next>__<story>_<name>.sql` on the `rwb_source_data` sequence (RD-P1-045); the name and number are Pending, owner database architect, NEW-GAP-S5-14.
4. Add the archive container health indicator outside API readiness.
5. Register `RetentionRunWorkflow` and its activities on the worker under a new build ID. Register no Schedule.
6. Add workload identity and least-privilege grants as in section 10. Principal and grant details remain Pending under GAP-0490, GAP-2429 and GAP-2430.
7. Configure batch size 5000 and the archive-container reference after the target is approved. Do not configure `rwb.retention.purge`.
8. Deploy with the flag off and run the smoke of section 4 step 8.
9. Publish the dashboard panels: run status, counts per table, container health. Capacity inputs (rows per run, bytes per row, growth horizon) and their approver are Pending, NEW-GAP-S5-14.
10. Publish the four alert rules of section 14, each with a runbook link and no personal data, delivered to the named owner within 15 minutes (NFR-068). Routes, thresholds, windows, owners and the missing-run window of JOB-17 are Pending, NEW-GAP-S5-13.
11. Promote the identical signed digest through DEV, SIT, UAT and PROD.
12. Rollback (RD-P1-045), in this order:
    1. Switch the feature flag of the change off.
    2. Only if the flag does not cover the fault, redeploy the previous image tag and chart version; the chart is shared, so the release note names every P1 capability the redeploy reverts.
    3. Never reverse a migration; correct a faulty one with a new forward version. No `U*.sql` and no down script exists.
    4. Every migration of the release works with the previous tag (expand-only), and the previous tag passes its smoke against the migrated schema in the pipeline.
    5. Workers use Worker Versioning: the previous build ID serves its pinned runs and no running workflow is terminated. Kafka offsets are not reset.
    6. On a first release, rollback is flag off and the worker scaled to zero; flagged operations answer 404.
    7. The release owner rolls back when post-deploy checks fail, when the platform smoke workflow (JOB-22) reports no result for the day, or when an incident is attributed to the release. A FAILED retention run is started again after the fix by a new `POST /retention-runs` with a new key (RD-P1-047).

**Done when.** AC1 to AC18 pass. Storage authorization, production approval, alert routing and the remaining delivery items stay Pending in section 20.

### 14. Validation and messages

| Code | Alert rule condition | Severity, threshold, window, route and config key |
|---|---|---|
| MSG-P1-020 | A run ends COMPLETED (information to Compliance) | Pending, NEW-GAP-S5-13 and NEW-GAP-S5-2 |
| MSG-GEN-006 | A run ends FAILED, or the archive container health indicator fails | Pending, NEW-GAP-S5-13 |
| MSG-P2-006 | A start is refused because the date is RUNNING or COMPLETED | Pending, NEW-GAP-S5-13 |
| MSG-P1-002 | A rule set is refused in full | Pending, NEW-GAP-S5-13 |
| Pending platform alert | Migration failure, probe failure, worker not polling, stuck run or expected run missing | Metric name, threshold, owner and route Pending, NEW-GAP-S5-13 |

Every scheduled job has an alert and runbook (NFR-067); alerts reach the assigned owner within 15 minutes (NFR-068). P1 does not own JOB-17's Schedule. Alert payloads contain no personal data. The message-to-route and threshold decisions are not inferred here.

### 15. Screens and states

The deployment serves the two contract operations and no screen of its own. The operator-facing surfaces of this story are the pipeline run view, the release view, the queue and scaler view, the dashboards and the runbook. Compliance reads a run in the running service through `GET /retention-runs/{runId}`, which the platform administration surface of another P1 story exposes, and the retention classes show on SCR-47 Personal data from Epic 8. The gateway-bff composite route (DP-19) is not on this path. Screen Specifications v1, section SCR-47, gives the states loading and list; the empty, error and no access states of SCR-47 are Not specified in the source documents (CG-ALL-2209; DOR-RWB-P1-E1017-OPS-10).

### 16. Test cases

- Test Cases v9 holds TC-P1-E1017-OPS-01 to -22 for this story; the criteria of section 7 cite the row that covers them.
- TC-P1-E1017-OPS-15 to -22 cover AC11 to AC18.

### 17. Guardrails

- No retention period is stored in code, values or database defaults; periods remain Pending with Compliance under GAP-1029.
- Only `interaction` can use ARCHIVE; the six other ruled tables use REVIEW/LISTED only; `case_list_row` is excluded by RD-P1-024 (X-01).
- P1's workload identity is not assigned until the archive target/prefix and grants are approved under GAP-0490.
- The deployment never sets the transaction-local `rwb.retention.purge` value.
- API readiness is not gated by archive-container health; container health has a separate signal.
- API and worker health are separate; worker minimum is zero and it polls one queue only.
- Migrations are forward-only and expand-only; rollback is flag off first, then the previous tag, with no down migration (RD-P1-045).
- No P1 retention Schedule is deployed; JOB-17 stays with rwb-document (ASM-0076).
- Logs, dashboards and alerts carry no personal data.

### 18. Traceability

| Requirement or decision | Deployment element | Test coverage |
|---|---|---|
| REQ-RDF-013 | Retention worker, archive identity, run dashboard and alerts | TC-P1-E1017-OPS-01 to TC-P1-E1017-OPS-08, TC-P1-E1017-OPS-13 to TC-P1-E1017-OPS-22 |
| RD-P1-047 | P1 REST start/read and P3 reads on the worker | TC-P1-E1017-OPS-04, TC-P1-E1017-OPS-17 |
| RD-P1-048 | ARCHIVE `interaction`; six REVIEW tables; periods Pending Compliance GAP-1029 | TC-P1-E1017-OPS-08 |
| RD-P1-024 (X-01) | Exclude `case_list_row` from P1 deployment | TC-P1-E1017-OPS-08, TC-P1-E1017-OPS-13 |
| NFR-067 / NFR-068 | Scheduled-job runbook/alert and 15-minute owner notification target | TC-P1-E1017-OPS-05, TC-P1-E1017-OPS-07, TC-P1-E1017-OPS-19 |
| NFR-075 / DL26 | Retention period remains Pending, owner Compliance | No test row until Compliance sets the period (GAP-1029) |
| GAP-0490, GAP-2429, GAP-2430 | Storage identity, service grants and payload codec remain Pending | Delivery follow-up |

### 19. Out of scope

- The application code of the run, the selection, the archive writer, the manifest check and the delete (RWB-P1-E1017-APP).
- The contract documents, the schemas and the fakes as published artefacts (RWB-P1-E1017-CON); this story only deploys the test copies.
- The retention rule, the retention action table and the monthly Schedule JOB-17 (RWB-P5-E1017-APP).
- The platform Temporal cluster, the namespace and its quotas (platform epics RWB-PLT-WF and RWB-PLT-E1071-CON).
- The write-once container, its immutability policy and its account (RWB-PLT-TE012-APP).
- Exact node pools, resource requests/limits, probe timings and KEDA thresholds are environment values; sizing details remain pending under GAP-2013 and the namespace detail under GAP-2010.
- The case legal hold and the holding logic (rwb-case, P3).
- The screen of SCR-47 Personal data and the platform administration surface that reads a run (Epic 8 and the P1 administration story).
- The cross-service proof of the run across P1, P3 and P5 (RWB-ITG-E1017-ITG).

### 20. Remaining delivery steps

- Size: Not specified; pending refinement. Owner: squad.
- Epic design sign-off: Pending. Owner: solution architect.
- CON Done: Pending. Owner: contract owner.
- Fake published: Pending. Owner: contract owner.
- Test data in DEV: Pending. Owner: QA.
- Archive container, P1 workload identity and prefix grant: Pending, GAP-0490. Owner: solution architect with platform security.
- Flag-off message code and switch-on order: Pending, NEW-GAP-S5-3. Owner: platform architect.
- PROD promotion approval path: Pending, NEW-GAP-S5-12. Owner: release manager.
- Metric names, alert severities, routes, thresholds and windows, named owners, the missing-run window and runbook links: Pending, NEW-GAP-S5-13. Owner: observability owner.
- Migration name and number, capacity inputs and approver: Pending, NEW-GAP-S5-14. Owner: database architect.
- Retention run record table: Pending, NEW-GAP-S5-8. Owner: data architect.
- Service-to-service rights and Temporal payload codec key: Pending, GAP-2429 / GAP-2430. Owner: platform security.
- Retention periods: Pending, GAP-1029. Owner: Compliance.
- NFR-075 ledger retention period: Pending under DL26. Owner: Compliance.
