# RWB-P1-AD019-OPS Data quality and reconciliation console

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Applied RD-P1-022, RD-P1-024, RD-P1-040, RD-P1-044 and RD-P1-045: a delta on the base release and on E1011-OPS, with no second worker, alert, dashboard or case-list resource.
- Fixed the review findings AD019-OPS#1–25: deployment ownership, switch, alerts, route, probes, secrets, dependencies, rollback, run books and test cases. Added AC8–AC10.
- Open: GAP-3502, GAP-3503, GAP-3273, GAP-2045 / ASM-3290, GAP-0728, GAP-3418 and GAP-3422.
- Cited the Test Cases v9 IDs of AC8–AC10, recorded the two retired test cases and moved the message standard citation to version 6.

| Item | Value |
|---|---|
| Story key | RWB-P1-AD019-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified |
| Patterns applied | DP05, DP10, DP19 |
| Parallel lane | L-P1-C |
| Ready to start | After RWB-P1-E1011-OPS and RWB-P1-AD019-APP |
| Depends on (build) | RWB-P1-E1015-OPS (base release), RWB-P1-E1011-OPS, RWB-P1-AD019-APP, RWB-P1-E1011-CON, platform flag library, RWB-PLT-N005-OPS |
| Contract dependencies | RWB-P1-E1011-CON; platform flag library |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-022; RD-P1-024; RD-P1-040; RD-P1-044; RD-P1-045 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v3.md (no FR mapped; no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: deployment side of the split of RWB-AD-019 for rwb-source-data: the api deployment with the reconciliation result read, the JOB-04 worker on the workflow kit, the gateway-bff route registration for SCR-45, the feature flag `rwb.source-data.reconciliation-run`, the four alert rules, the dashboard and the health checks, the runbook and the rollback (DP05, DP10, DP19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-AD019-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (10 resolved, 11 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: P1 developer readiness (RD-P1 register); story editor S9-stories.

### 1. Story

As a **platform engineer (RW-TRIBE)**, I want **the AD019 console delta deployed on the existing E1011 reconciliation service, with its feature-flag registration, console result panel and runbook links**, so that **operators can inspect reconciliation results without a duplicate workflow, dashboard or case-list service**.

RWB-P1-E1015-OPS is the base release (chart, Deployments, probes, migration job, KEDA and the Load late, Load failed and stale alerts). RWB-P1-E1011-OPS owns the `ReconciliationWorkflow` and activity `reconciliation` deployment and the Reconciliation break alert. AD019-OPS adds the console-read flag and panel to the existing service deployment. It adds no reconciliation activity, schedule, consumer group or case-list deployment (RD-P1-022, RD-P1-024, X-08).

### 2. Business rationale

This is an operations delta on RWB-P1-E1011-OPS. E1011-OPS remains responsible for the reconciliation worker, activity `reconciliation` and Reconciliation break alert. AD019-OPS adds the console-read flag and a panel to the existing service dashboard; it does not deploy a second worker or dashboard.

Case-list ownership remains with rwb-case. The P3 key-list contract path is Pending GAP-3273. Metric names and labels remain Pending GAP-2045 / ASM-3290, so the panel cannot claim an executable metric until the observability owner publishes them.

### 3. Preconditions

- RWB-P1-E1011-OPS deploys the only P1 reconciliation worker and owns the Reconciliation break alert.
- RWB-P1-AD019-APP provides the console query delta over the result read published by RWB-P1-E1011-CON, version `rwb-source-data.yaml` 5.1.0.
- The platform flag library holds `rwb.source-data.reconciliation-run`, registered by this story (RD-P1-044). It starts, stops and skips no reconciliation run; the run is gated by `rwb.source-data.daily-gate` of E1011. The run is not started by an event, so no business date is consumed or lost while a switch of this story is off. Pending: which operations the switch gates (AD019 publishes none of its own), owner solution architect, GAP-3502; and the permission and audit record of a switch change, owner platform flag owner, GAP-3503.
- The rwb-source-data service dashboard already exists; AD019 adds a panel to it, not a second dashboard.
- Case list and case-key operations are owned by rwb-case; the key-list path used by REC-05 is Pending GAP-3273. The SCR-45 composite route is delivered by RWB-P3-AD019-APP against RWB-PLT-N001-CON; its path and merge and error rules are Pending, owner solution architect, tracked as GAP-0728.
- Metric names and labels needed by the console panel remain Pending GAP-2045 / ASM-3290.
- Environments are DEV, SIT, UAT and PROD. This story adds no secret, certificate, credential, migration or consumer group.

### 4. Flow

1. Add the AD019 values keys to the base chart for DEV, SIT, UAT and PROD; create no second api or worker deployment and change no probe, scaler or secret.
2. Register `rwb.source-data.reconciliation-run` with the platform flag library. It changes no reconciliation run; its gated operations are Pending under GAP-3502.
3. Add the console result panel to the existing rwb-source-data service dashboard. The metric names and labels remain Pending GAP-2045 / ASM-3290.
4. Keep the reconciliation worker, `ReconciliationWorkflow`, activity `reconciliation`, run record, and Reconciliation break alert under RWB-P1-E1011-OPS.
5. Register no route: the SCR-45 composite route of RWB-P3-AD019-APP calls rwb-case reads, and rwb-case calls the P1 result read.
6. Link the console panel to the JOB-04 run book of RWB-PLT-E1056-OPS (`docs/operations/runbooks/JOB-04.md`). A FAILED run is rerun with `POST /admin/jobs/{jobId}/rerun` (RWB-P1-AD018-CON, Platform administration U); held or stale inputs and worker faults follow the E1011-OPS and E1015-OPS entries.
7. Roll back per RD-P1-045: switch the flag off first; only if the fault remains, redeploy the previous image tag and chart version (the release note names every P1 capability this reverts); never reverse a migration. Running workflows are not terminated.

### 5. Exception paths

| ID | Trigger | What happens | Owner |
|---|---|---|---|
| X1 | E1011 result read unavailable | Base and E1011 health and alert behaviour applies; the console shows its error state for that block | RWB-P1-E1011-OPS |
| X2 | P3 case-key list path unavailable or unpublished | REC-05 open-case key comparison stays blocked; no P1 case-list fallback is allowed | GAP-3273; rwb-case service owner |
| X3 | Console metrics are not published | Panel wiring remains pending; no invented metric name is deployed | GAP-2045 / ASM-3290; observability owner |
| X4 | Flag library or permission contract unavailable | Do not switch the AD019 flag on until its provider and authorisation are available | Platform flag owner |
| X5 | The chart diff changes an object this story does not own | The release is refused | DevOps team |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Extends E1011 deployment, flag registration and service dashboard |
| Negotiable | No worker or alert ownership is moved from E1011-OPS |
| Valuable | Makes the existing reconciliation result visible to the console operators |
| Estimable | One flag registration, one dashboard panel, run book link and smoke tests |
| Small | No new chart, worker, migration, route or dashboard |
| Testable | Deployment and flag artifacts are checked against their owning contracts |

### 7. Acceptance criteria

```gherkin
Feature: AD019 operational delta

  Scenario: AC1 Delta uses the E1011 deployment
    Given the E1011 service and worker deployments are available
    When the AD019 release is applied
    Then the result-read configuration is added to the existing deployment
    And no second reconciliation worker or activity is registered

  Scenario: AC2 Feature flag is registered on the existing service
    Given the platform flag library is available
    When `rwb.source-data.reconciliation-run` is registered and then switched off
    Then the flag exists for rwb-source-data in DEV, SIT, UAT and PROD
    And no reconciliation run is started, stopped or skipped by it
    And its gated operations (GAP-3502) and change permission and audit (GAP-3503) stay Pending

  Scenario: AC3 Console panel extends the service dashboard
    Given the approved metrics for reconciliation results are published
    When the dashboard configuration is applied
    Then the console panel is added to the existing rwb-source-data dashboard
    And no second service dashboard is created
    And metric names and labels are those published under GAP-2045 and no label holds a customer or account value

  Scenario: AC4 Gateway composition uses owner contracts
    Given the SCR-45 composite route of RWB-P3-AD019-APP
    When the route configuration of this release is checked
    Then this release registers no route and no gateway upstream
    And the route calls rwb-case reads only and rwb-case calls the E1011-CON result read
    And no P1 case table is configured
    And the route path and merge rules remain Pending GAP-0728

  Scenario: AC5 AD019 adds no reconciliation worker or case-list resources
    Given the deployed Temporal registrations and service database
    When they are compared with RD-P1-022 and RD-P1-024
    Then only E1011 owns `ReconciliationWorkflow` and activity `reconciliation`
    And no AD019 activity, case-list table, case-list Schedule or case-list workflow exists

  Scenario: AC6 P3 key-list dependency is explicit
    Given REC-05 needs open-case account and party keys
    When the deployment dependency list is reviewed
    Then the consumer is the rwb-case key-list contract
    And its path remains Pending GAP-3273 with owner rwb-case service owner

  Scenario: AC7 Release rollback follows the existing E1011 procedure
    Given an AD019 release on top of a recorded previous image tag and chart version
    When it is rolled back
    Then the flag is switched off first and the previous tag is redeployed only if the fault remains
    And the previous tag passes its smoke test against the current schema
    And no down migration runs, no workflow is terminated and the reconciliation_result rows are unchanged

  Scenario: AC8 Chart diff shows only AD019 additions
    Given the rendered chart of the previous release and of this release
    When the two are compared
    Then the only changes are the AD019 values keys, flag and panel
    And no Deployment, probe, scaler, secret, consumer group, Schedule, workflow registration or alert rule changes

  Scenario: AC9 No secret or personal data in the delta
    Given the rendered values, the image, the panel definition and the smoke logs
    When they are scanned
    Then no secret value and no account, person or customer value is found

  Scenario: AC10 Run book link and rerun step
    Given the console panel and the JOB-04 run book
    When the release check follows the panel link
    Then the run book opens and its rerun step names POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun with Platform administration U
```

Test references: AC1 TC-P1-AD019-OPS-01; AC2 TC-P1-AD019-OPS-05; AC3 TC-P1-AD019-OPS-06; AC4 TC-P1-AD019-OPS-07; AC5 TC-P1-AD019-OPS-08; AC6 TC-P1-AD019-OPS-09; AC7 TC-P1-AD019-OPS-03. Test Cases v9 holds the rows for the changed texts of AC2, AC3, AC4 and AC7.

AC8 TC-P1-AD019-OPS-10; AC9 TC-P1-AD019-OPS-11; AC10 TC-P1-AD019-OPS-12 (Test Cases v9).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | E1011-OPS owns the reconciliation worker, activity and Reconciliation break alert | RD-P1-022; RD-P1-040 |
| BR2 | AD019-OPS adds only its values keys, flag, dashboard panel and run book link to the base release | RD-P1-044 |
| BR3 | No AD019 activity, case-list table, Schedule, consumer group or second dashboard is deployed | RD-P1-024; RD-P1-040 |
| BR4 | The SCR-45 route calls rwb-case reads and rwb-case calls the P1 result read; this story registers no route | RWB-P3-AD019-APP; RD-P1-024 |
| BR5 | Metric names and labels remain pending GAP-2045 / ASM-3290 | Review finding AD019-OPS#4 |
| BR6 | Alerts: Reconciliation break by RWB-P1-E1011-OPS; Load late, Load failed and stale by RWB-P1-E1015-OPS; this story declares no alert rule | RD-P1-044 |
| BR7 | Rollback is flag off first, then the previous tag; migrations are forward only | RD-P1-045 |

### 9. State transitions

This deployment delta adds no workflow state machine. The reconciliation workflow lifecycle remains owned by RWB-P1-E1011-OPS and its Temporal contract. The console flag does not create or publish a case-list state.

### 10. Authority

| Role | Responsibility |
|---|---|
| RWB-P1-E1011-OPS owner | Reconciliation worker, workflow registration, Reconciliation break alert and its run book entries |
| RW-PLATADM, RW-SECADM (Platform administration U) | Rerun a FAILED run through RWB-P1-AD018-CON |
| AD019-OPS owner | Console-read flag and panel additions to existing deployment/dashboard |
| rwb-case owner | Case-list and open-case key-list contract |
| Platform flag owner | Flag library, permission and audit contract |
| Observability owner | Metric names, labels and alert/dashboard source |
| rwb-case and gateway-bff owners | SCR-45 composite route (RWB-P3-AD019-APP, RWB-PLT-N001-CON) |

### 11. Data

| Resource | Owner | AD019-OPS treatment |
|---|---|---|
| `reconciliation_result` and `job_run` records | P1 E1011 / AD018 | Observe through the existing service; no OPS writes |
| Case list and open-case keys | P3 rwb-case | Access through owner contracts only |
| Console flag `rwb.source-data.reconciliation-run` | RWB-P1-AD019-OPS, platform flag library | Register through the flag library; no local flag table |
| Metrics and dashboard | Platform observability | Panel added to existing service dashboard; names pending GAP-2045 / ASM-3290 |

No table, migration or case-list resource is created by AD019-OPS.

### 12. Contract

#### 12.1 Service contract

The deployed result read is owned and published by RWB-P1-E1011-CON, `rwb-source-data.yaml` 5.1.0. AD019-OPS deploys no API of its own.

#### 12.2 Gateway composition

SCR-45 is the composite route of RWB-P3-AD019-APP over rwb-case reads; rwb-case calls the E1011 result read. AD019-OPS adds no route and no upstream.

#### 12.3 Events published

None by AD019-OPS.

#### 12.4 Events consumed

None by AD019-OPS. The E1015/E1011 event chain is provisioned by its owning stories; AD019 creates no consumer group.

#### 12.5 Workflows and activities

No AD019 workflow or activity. RWB-P1-E1011-OPS owns the single registered activity `reconciliation` on `ReconciliationWorkflow`.

#### 12.6 Schedules

No AD019 schedule. rwb-case owns the case-list schedule.

#### 12.7 Tables

No AD019 table or migration. Existing `job_run`, `job_run_check` and `reconciliation_result` remain owned by their APP stories. No P1 case-list table exists.

#### 12.8 Contract fakes

Non-production smoke uses the version-pinned E1011-CON provider fake and rwb-case consumer fake. Production values contain no fake fixtures.

#### 12.9 Call-type summary

| Call type | Detail |
|---|---|
| REST | Existing E1011 result read and gateway-bff composition |
| Kafka | No AD019 consumer |
| Temporal | E1011 workflow only; no added activity |
| File | None |

### 13. Solution plan

**Artifacts:** AD019 values keys on the base chart, flag registration, one panel on the existing service dashboard and the run book link. The run window and completion alarm of JOB-04 are those of E1011-OPS (Pending GAP-3422); read latency and error alerts are the base release's.

**Do not create:** second worker or API deployment, new workflow/activity, service dashboard, P1 gateway route, case-list table, Schedule, consumer group, migration or alert owner for the Reconciliation break.

**Pending inputs:** metric names and labels (GAP-2045 / ASM-3290), P3 key-list path (GAP-3273), gated operations (GAP-3502), flag permission and audit record (GAP-3503) and route rules (GAP-0728).

### 14. Validation and messages

AD019-OPS introduces no business message. Reconciliation and access errors use E1011-CON and the shared Problem schema. The Reconciliation break alert remains owned by E1011-OPS and carries MSG-P1-012 per Error and Message Standard v6; its destination and balance placeholders are Pending GAP-3418. The stale alert (MSG-P1-001) is that of E1015-OPS. No case-list alert or message is deployed by this delta.

### 15. Screens and states

SCR-45 is the composite route of RWB-P3-AD019-APP; rwb-case supplies its reads from, among others, the E1011 result read. AD019-OPS adds one panel to the existing rwb-source-data service dashboard. It does not deploy a separate dashboard or console screen. Panel metrics remain Pending GAP-2045 / ASM-3290.

### 16. Test cases

| AC | Test reference |
|---|---|
| AC1–AC3 | TC-P1-AD019-OPS-01, TC-P1-AD019-OPS-05, TC-P1-AD019-OPS-06 |
| AC4–AC7 | TC-P1-AD019-OPS-07, TC-P1-AD019-OPS-08, TC-P1-AD019-OPS-09, TC-P1-AD019-OPS-03 |
| AC8, AC9, AC10 | TC-P1-AD019-OPS-10, TC-P1-AD019-OPS-11, TC-P1-AD019-OPS-12 |

Test Cases v9 holds the rows of the changed criteria (AC2, AC3, AC4, AC7); TC-P1-AD019-OPS-02 and TC-P1-AD019-OPS-04 are retired there and are not cited.

### 17. Guardrails

- E1011-OPS remains the only owner of the reconciliation workflow deployment and Reconciliation break alert.
- No new AD019 activity, worker, case-list table, Schedule, consumer group or dashboard is deployed.
- The P1 case list and case keys are never read by direct access to P3 tables.
- The result read follows E1011-CON 5.1.0.
- Do not fabricate metric names, alert thresholds, message IDs or flag audit behavior.
- Rollback is flag off first, then the previous tag; migrations are forward only and existing run and result rows stay (RD-P1-045).

### 18. Traceability

| Requirement | Source | Test reference |
|---|---|---|
| Console delta deployment extends E1011 | RD-P1-022; RD-P1-044 | TC-P1-AD019-OPS-01 |
| P1 does not own the case list | RD-P1-024 | TC-P1-AD019-OPS-08 |
| No duplicate reconciliation activity | RD-P1-040 X-08 | TC-P1-AD019-OPS-08 |
| Dashboard metric names and labels | Pending GAP-2045 / ASM-3290 | TC-P1-AD019-OPS-06 |

### 19. Out of scope

- Reconciliation worker, activity `reconciliation` and Reconciliation break alert (RWB-P1-E1011-OPS).
- Reconciliation calculations and result writes (RWB-P1-E1011-APP).
- P1 case-list data, schedule or copied table (rwb-case; RD-P1-024).
- SCR-45 page and composite route (RWB-P3-AD019-APP, RWB-PLT-N001-CON).
- Unpublished metrics, labels, thresholds or flag authorization behavior (GAP-2045 / ASM-3290; platform flag owner).

### Remaining delivery steps

- Size: Pending squad refinement; owner delivery lead.
- Epic design sign-off: Pending; owner solution architect.
- CON Done: Pending; owner contract owner.
- Contract fake published at the approved version: Pending; owner contract owner.
- Synthetic test data in DEV: Pending; owner test data owner.