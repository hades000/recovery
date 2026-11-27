# RWB-P1-AD018-OPS Interface and job monitor

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Applied RD-P1-004, RD-P1-012, RD-P1-020, RD-P1-021, RD-P1-024, RD-P1-040, RD-P1-044 and RD-P1-045: delta on the base release, one owner per deployed object, flag-first rollback.
- Fixed the review findings AD018-OPS#1–23: chart delta, alerts, grants, dependencies, route, run books, switch, rollback, states and test cases. Added AC11–AC14.
- Open: GAP-3499, GAP-3500, GAP-3505 and GAP-2164 (threshold values).
- Cited the Test Cases v9 IDs of AC11–AC14 and moved the message standard citation to version 6.

| Item | Value |
|---|---|
| Story key | RWB-P1-AD018-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | L-P1-B |
| Ready to start | After RWB-P1-AD018-APP and RWB-P1-E1015-OPS |
| Size | Not specified |
| Depends on (build) | RWB-P1-AD018-APP, RWB-P1-AD018-CON, RWB-P1-E1015-OPS (base release), RWB-PLT-N001-CON, RWB-PLT-E1056-OPS, P2 scheduled-jobs contract |
| Contract dependencies | RWB-P1-AD018-CON; P2 scheduled-jobs contract; RWB-P1-E1015-CON; platform flag library |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-004; RD-P1-012; RD-P1-020; RD-P1-021; RD-P1-024; RD-P1-040; RD-P1-044; RD-P1-045 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v3.md (no FR mapped; no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-018 for rwb-source-data. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 11 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: P1 developer readiness (RD-P1 register); story editor S9-stories.

### 1. Story

As a **platform engineer (RW-TRIBE)**, I want **the AD018 P1 job monitor deployed with the APP-owned run-table migration, P2 catalogue contract, service probes, alerting and runbooks**, so that **operators can see P1 run outcomes and safely rerun failed work**.

This story deploys the APP behavior and migration defined by RWB-P1-AD018-APP and the sole job contract published by RWB-P1-AD018-CON. P1 creates no `job_catalog`, case-list table, `CaseListBuildWorkflow` or `DailyCaseList` schedule. Other services' job operations are composed by gateway-bff (RD-P1-012, RD-P1-020, RD-P1-021, RD-P1-024).

### 2. Business rationale

The deployment makes P1 run history and rerun available through the AD018 contract. The APP story owns the migration and runner behavior; OPS runs the migration and deploys the artifact. P2 owns the catalogue, and the service reads it through P2's scheduled-jobs contract.

A FAILED run, or a run past its threshold, is alerted by the rule of RWB-PLT-E1056-OPS (MSG-P2-004 to the owner role of the job and RW-PLATADM); the stale, Load late and Load failed alerts are those of RWB-P1-E1015-OPS and the Reconciliation break alert is that of RWB-P1-E1011-OPS (RD-P1-044). This story adds no second alert for any of these signals. WAITING means a mapped source is not `COMPLETED`; it is visible and informational. Alerts on outbound files belong to rwb-integration. P1 does not operate ACE batches or case-list resources.

### 3. Preconditions

- RWB-P1-AD018-CON publishes `rwb-source-data.yaml` 5.1.0.
- RWB-P1-AD018-APP owns the `job_run` and `job_run_check` migration; OPS runs it in the per-service migration sequence (RD-P1-020).
- P2 scheduled-jobs contract and `GET /api/recovery/integration/v1/admin/scheduled-jobs` are available for P2-owned `job_catalog` metadata (RD-P1-021).
- RWB-P1-E1015-OPS is the base release: the rwb-source-data chart, api and worker Deployments, probes, migration job, Key Vault secret references, workload identity and KEDA scaling exist. This story adds values keys only (RD-P1-044).
- Environments are DEV, SIT, UAT and PROD. Alert thresholds, channels, replica counts and resource sizes are per-environment values-file entries (GAP-2164, ASM-3468).
- RWB-PLT-E1056-OPS holds the job catalogue rows, the failed-job alert and the run book file of each job.
- Pending: how synthetic ACE batch rows and a FAILED run are provided in SIT and UAT, with which test identity and clean-up, owner test data owner with the ACE team lead, tracked as GAP-3505.

### 4. Flow

1. Build and scan the APP image and render the base chart of RWB-P1-E1015-OPS with the AD018 values keys for DEV, SIT, UAT and PROD.
2. Verify the rwb-source-data login: rights on `rwb_source_data`, SELECT on the approved read-only `recovery.v_ace_*` views including `v_ace_batch_status`, and no right on `public` or another service schema.
3. Run the APP-owned Flyway migration that creates `job_run` and `job_run_check`; fail the deployment on migration failure. OPS does not author or claim the migration.
4. Deploy the image through the base release's api and worker Deployments, pinned by digest, with secret references only. This story adds no Deployment, probe, scaler or worker registration.
5. Confirm the job-list and rerun endpoints conform to `rwb-source-data.yaml` 5.1.0 and the P2 catalogue call uses its contract fake or published endpoint.
6. Register `rwb.p1.jobmonitor` with the platform flag library with its values per environment; run the endpoint smoke only where it is on. Pending: initial value and enabling role per environment, owner solution architect with the release owner, tracked as GAP-3499.
7. Add panels for P1 run statuses and check outcomes to the existing rwb-source-data dashboard. A WAITING run does not page. Pending: metric names, types, labels (no customer or account value) and the emitting component in RWB-P1-AD018-APP, owner observability owner, tracked as GAP-3500.
8. Register the gateway-bff composite route for SCR-44 against the route contract of RWB-PLT-N001-CON (GAP-0516, ASM-0708); P1 calls no other service's job operation. In the JOB-04 run book of RWB-PLT-E1056-OPS, check that the restart step names the rerun with the run ID, no body and a UUID Idempotency-Key.
9. Roll back per RD-P1-045: switch `rwb.p1.jobmonitor` off first; only if the fault remains, redeploy the previous image tag and chart version (the release note names every P1 capability this reverts); never reverse a migration. The previous tag passes its smoke test against the migrated schema.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | The chart diff changes an object another story owns (workflow, Schedule, topic, consumer group, probe or alert) | The release is refused | None | AC4 |
| X3 | A grant on `public` or another schema, or a job entry for the retired JOB-01 or JOB-09 | The release is refused | None | AC4, AC11 |
| X4 | A P1 run is FAILED or past its threshold | The alert of RWB-PLT-E1056-OPS reaches the owner role and RW-PLATADM | MSG-P2-004 | AC5 |
| X5 | A run waits because an ACE batch is late | The WAITING count shows on the panel; no page from this story; the stale and Load late alerts are those of RWB-P1-E1015-OPS | MSG-P1-001 | AC5 |
| X6 | A rerun is refused with 409 | The run is not FAILED or another run is open (MSG-P1-011), or the ACE batch is not `COMPLETED` (MSG-P1-001); the JOB-04 run book names both causes | MSG-P1-011 / MSG-P1-001 | AC6 |
| X7 | A product is STALE, including one with no business date | Alert and message are those of RWB-P1-E1015-OPS; this story declares none | MSG-P1-001 | AC5 |
| X8 | The monitor read fails or is slow | The service error rate and latency alerts of the base release apply; the composite route is checked before the service | None | AC13 |
| X9 | The smoke step cannot see the second run after a rerun | The release stops; the run rows and the Idempotency-Key are checked | None | AC6 |
| X10 | The SCR-44 route cannot be registered | The release stops and the previous route version stays | None | AC13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Delta on the base release; uses the platform observability stack and the published contract; builds no application code |
| Negotiable | Replica counts, resource sizes, retention and alert thresholds are environment values, not story decisions |
| Valuable | Turns the monitor into an operated capability with panels, a route and a checked rerun path |
| Estimable | Values keys, one migration run, panels, one route registration, one flag and smoke tests |
| Small | Fits one sprint with the run books |
| Testable | Each criterion checks a chart diff, a grant, a panel, an alert delivery, a route answer or a smoke result |

### 7. Acceptance criteria

```gherkin
Feature: AD018 P1 job monitor deployment

  Scenario: AC1 Owned run tables are migrated before readiness
    Given the APP migration creates job_run and job_run_check
    When the deployment migration runs
    Then both tables and RD-P1-020 constraints exist before the API is ready
    And existing run rows are unchanged

  Scenario: AC2 Deployment uses approved identity and grants
    Given the rendered chart and database grants
    When the chart is applied
    Then secrets are Key Vault references and the image digest is pinned
    And the login has rights on rwb_source_data and SELECT on the approved recovery.v_ace_* views only
    And the probes of the base release are unchanged

  Scenario: AC3 Pipeline validates the published contract
    Given commit artifacts and `rwb-source-data.yaml` 5.1.0
    When the deployment pipeline runs
    Then build, scan, migration and smoke stages validate the same contract version
    And the promoted artifact digest matches the tested digest

  Scenario: AC4 P1 deploys no cross-service jobs or case-list artifacts
    Given the rendered chart of the base release and of this release
    When the two are compared
    Then no workflow registration, Schedule, topic, consumer group, probe or alert rule owned by another story changes
    And no case-list workflow, schedule or table and no foreign job operation is provisioned
    And no job entry names the retired JOB-01 or JOB-09

  Scenario: AC5 Failed and waiting run alerts differ
    Given a synthetic FAILED run and a synthetic WAITING run
    When alert rules evaluate them
    Then the RWB-PLT-E1056-OPS rule sends MSG-P2-004 for the FAILED run to the owner role and RW-PLATADM within the NFR-068 target
    And the WAITING run is shown on the panel and pages nobody
    And this release adds no second alert rule for either signal

  Scenario: AC6 Rerun smoke uses the published contract
    Given a FAILED run, a COMPLETED ACE batch and a user with Platform administration U
    When the smoke invokes rerun with UUID Idempotency-Key
    Then a 202 creates one new PENDING run with runNo increased by one and preserves the failed row, and the list returns both
    And an incomplete batch answers 409 MSG-P1-001 without a new row

  Scenario: AC7 Migration failure stops release
    Given the migration fails
    When deployment runs
    Then the pipeline stops, the new version receives no traffic and the prior image remains serving

  Scenario: AC8 Rollback retains forward schema and run evidence
    Given version N is deployed and its forward-only migration is applied
    When version N-1 is restored after the flag is disabled
    Then existing run rows are unchanged and no down migration runs

  Scenario: AC9 Secret and personal-data scan passes
    Given rendered charts, values, images, logs and smoke data
    When the pipeline scans them
    Then no secret value or personal data field is present

  Scenario: AC10 Production values exclude fakes and smoke seeds
    Given production values
    When the release chart is rendered
    Then no contract fake, fixture or synthetic seed is configured

  Scenario: AC11 Grants outside the service are refused
    Given the rwb-source-data login in SIT
    When it selects from a table in public and from another service's schema
    Then both are refused
    And a select from recovery.v_ace_batch_status succeeds

  Scenario: AC12 Feature switch
    Given rwb.p1.jobmonitor is off
    When GET /api/recovery/source-data/v1/admin/jobs is called by RW-PLATADM
    Then the answer is 404 MSG-P4-003
    And with the switch on the answer is 200

  Scenario: AC13 Composite route and access
    Given the SCR-44 route is registered
    When it is called without a session and then by a role without Platform administration R
    Then the answers are 401 MSG-P4-001 and 403 MSG-P4-002

  Scenario: AC14 Run book restart step
    Given the JOB-04 run book of RWB-PLT-E1056-OPS
    When the release check reads its restart step
    Then it names POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun with the run ID, no body and a UUID Idempotency-Key
```

Test references: AC1–AC6 TC-P1-AD018-OPS-01 to -06; AC7 TC-P1-AD018-OPS-08; AC8 TC-P1-AD018-OPS-09; AC9 TC-P1-AD018-OPS-10; AC10 TC-P1-AD018-OPS-11; section 12.7 boundary TC-P1-AD018-OPS-07. Test Cases v9 holds the rows for the changed texts of AC2, AC4, AC5 and AC6.

AC11 TC-P1-AD018-OPS-12; AC12 TC-P1-AD018-OPS-13; AC13 TC-P1-AD018-OPS-14; AC14 TC-P1-AD018-OPS-15 (Test Cases v9).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login per service and no ACE credential in the release; rights on `rwb_source_data` and SELECT on the approved `recovery.v_ace_*` views only | DP-02; RWB-P1-E1069-APP |
| BR2 | The per-service Flyway sequence owns the schema objects the release needs, and no other service's schema is touched | DP-15; ADR-021 |
| BR3 | The release declares no object another story owns: no workflow, Schedule, topic, consumer group, probe or alert rule | RD-P1-044 |
| BR4 | No release adds a path, a credential or a job name that can start, stop or rerun an ACE batch, a feed or a file | RWB-AD-018 guardrail; NFR-015 |
| BR5 | A FAILED run is alerted by RWB-PLT-E1056-OPS (MSG-P2-004) within the NFR-068 target, which stays Proposed under open decision DL11; a WAITING run pages nobody | NFR-068; DL11; RD-P1-044 |
| BR6 | Every threshold, channel and owner is a values-file or catalogue entry, never code; apart from the 15-minute failed-job alert of BR5, which comes from NFR-068, the alert thresholds, panel baselines, channels, replica counts and resource sizes are Not specified in the source documents (GAP-2164), so each is held per environment in the values file | NFR-067; Template and Rules §R7.2 s17; GAP-2164 |
| BR7 | One artefact is promoted through the three environments without a rebuild | ADR-023; Template and Rules §R8 |
| BR8 | The monitor reads identifiers, codes, dates, counts and durations only; no personal data reaches a panel, a log line or a trace | Template and Rules §R7.2 s17 |
| BR9 | No data lake, no ADF job and no inbound load path is deployed for this capability | DP-17; RWB-P1-E1069-APP; FSD P1 v3 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Pipeline run | The pipeline and the boundary assertions pass | Deployed to DEV |
| Deployed to DEV | Promotion | The smoke profile passes | Deployed to SIT |
| Deployed to SIT | Promotion | The smoke profile, the panels and one alert per rule pass | Deployed to UAT |
| Deployed | FAILED run | The alert of RWB-PLT-E1056-OPS fires | Alerted, run book opened |
| Alerted | Rerun or restart | The latest run of the job and date is COMPLETE | Recovered, the alert closes |
| Deployed | Release changes an object it does not own | The chart diff check fails | Release refused; the previous version keeps running |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps team | Owns the AD018 values keys, the migration run, the panels, the route registration and the switch registration |
| RW-PLATADM, RW-SECADM | Operate the monitor and the rerun in the environment (Platform administration U) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read the monitor (Platform administration R) |
| Owner role of a catalogue row | Receives the failed-job alert of RWB-PLT-E1056-OPS |
| Platform observability owner | Owns the metrics, panels, alerts and traces this story consumes |
| No role | Reruns an ACE batch, a feed or a file, or deploys a second source of truth for the wait state |

### 11. Data

| Item | Owner | Deployment responsibility |
|---|---|---|
| `job_run`, `job_run_check` | P1 `rwb_source_data` | Run APP-authored migration; no OPS DDL |
| `job_catalog` | P2 `rwb_integration` | No P1 migration or table grant; APP reads P2 contract |
| `data_product_load` | P1 `rwb_source_data` | Read-only for monitor; E1015-APP writes |
| `recovery.v_ace_*` views | ACE source through P1 view contract | Read-only grants for service login |

Schema fields and IDs are those in RD-P1-020; no case-list table is deployed (RD-P1-024).

### 12. Contract

#### 12.1 API deployment

Deploy the provider contract `rwb-source-data.yaml` 5.1.0 from RWB-P1-AD018-CON. The job list and rerun paths and their responses are not redefined here.

#### 12.2 Consumed contracts

Use the P2 scheduled-jobs contract for `GET /api/recovery/integration/v1/admin/scheduled-jobs`. Do not provision a P1 `job_catalog` table or read P2 schema directly.

#### 12.3 Events published

None by OPS.

#### 12.4 Events consumed

No AD018 consumer group is added. The event types `AceDataReady` and `AceDataLate` are published on topic `rwb.source-data.events.v1` by E1015-APP.

#### 12.5 Workflows

None. `AceIngestCheck` is registered by RWB-P1-E1015-OPS, `ReconciliationWorkflow` by RWB-P1-E1011-OPS, `RetentionRunWorkflow` by RWB-P1-E1017-OPS and `Stage2ProductWorkflow` by RWB-P1-E2010-OPS (RD-P1-044). No case-list workflow is registered.

#### 12.6 Schedules

No case-list Schedule is provisioned.

#### 12.7 Tables

OPS runs the APP migration for `job_run` and `job_run_check`. `job_catalog` remains P2-owned. Freshness data is read only. No case-list table is deployed.

#### 12.8 Fakes and smoke fixtures

Non-production smoke uses version-pinned P2 and P1 contract fakes and synthetic run rows. Production values contain no fake or synthetic data.

#### 12.9 Call-type summary

| Call type | Deployment action |
|---|---|
| REST | Deploy P1 job-list and rerun operations; consume P2 scheduled-jobs contract from the app |
| Kafka | No AD018 consumer group |
| Temporal | No registration; existing P1 workflows are registered by their OPS stories |
| File | None |

### 13. Solution plan

**Deployment** is a delta on the base release of RWB-P1-E1015-OPS: AD018 values keys, the APP migration, the flag, the panels and the SCR-44 route registration.

**Pipeline stages:** build, unit and contract tests, image scan (fails on a Critical finding), APP migration, deploy, smoke, chart diff check, promotion of the same digest. Migration failure stops promotion. Rollback follows step 9; no down migration runs.

**Monitoring and run books:** panels distinguish FAILED from WAITING and show run status, check code and business date. Alerts and run book files are those of the owning stories (section 2); this story writes no second run book file. The run book states that ACE batches are not operated by P1.

**Feature switch.** `rwb.p1.jobmonitor`, registered with the platform flag library; switching it off is the first rollback action (RD-P1-045). Initial value and enabling role per environment: GAP-3499.

### 14. Validation and messages

Rerun errors follow AD018-CON and Error and Message Standard v6: 400 `MSG-PLT-N009-03`, 404 `MSG-P4-003`, 409 `MSG-P1-011`, `MSG-P1-001` or `MSG-PLT-N009-05`, and 503 `MSG-GEN-006`. Access failures answer 401 `MSG-P4-001` and 403 `MSG-P4-002`. The failed-job alert carries MSG-P2-004. This story adds no message text or ID. Alert thresholds and channels remain values-file entries under GAP-2164 / ASM-3468; The FAILED target is NFR-068, Proposed under DL11.

### 15. Screens and states

SCR-44 Interface and job monitor in its four states — Running, failed, waiting for the ACE batch, complete — is served through the gateway-bff composite route (DP-19). This story proves the four states in the SIT smoke profile and in the panels; it builds no screen and fixes no field, and the panels of the app story are its only consumer. The other states of SCR-44 are these. Empty: a plain sentence saying there is nothing to show, and the action to take if one applies. Loading: skeleton rows while data arrives, with no spinner over the whole page. Error: the message from the error and message standard next to the field or at the top. No access: a role without the Platform administration right is refused with MSG-P4-002. This story registers the gateway-bff composite route for SCR-44 and its alerts; RWB-P1-AD018-APP serves the reads and RWB-P1-AD018-CON publishes them (GAP-0516).

### 16. Test cases

| AC | Test reference |
|---|---|
| AC1–AC6 | TC-P1-AD018-OPS-01 to TC-P1-AD018-OPS-06 |
| AC7–AC10 | TC-P1-AD018-OPS-08 to TC-P1-AD018-OPS-11 |
| Section 12.7 tables | TC-P1-AD018-OPS-07 |
| AC11, AC12 | TC-P1-AD018-OPS-12, TC-P1-AD018-OPS-13 |
| AC13, AC14 | TC-P1-AD018-OPS-14, TC-P1-AD018-OPS-15 |

Test Cases v9 holds the rows of the changed criteria (AC2, AC4, AC5, AC6).

### 17. Guardrails

- No business value in the chart or the code: job names, cadences, expected durations, alert minutes, owners and thresholds are catalogue or values rows.
- No personal data in a panel, a log line, a trace or a run book: identifiers, codes, dates, counts and durations only.
- One login for the service and no ACE credential; no grant on `public` and no cross-schema access (DP-01, DP-02, DP-05).
- No release adds a path, a credential or a job name that can start, stop or rerun an ACE batch, a feed or a file.
- No topic, consumer group or Schedule is declared by this release; the service topic stays as its owner provisioned it.
- No data lake, no ADF job and no inbound load path is deployed (DP-17).
- Every threshold, channel and owner is a values-file or catalogue entry, and the chart check of AC4 fails a release that adds an object it does not own.

### 18. Traceability

| Requirement | Source | Test reference |
|---|---|---|
| P1 job list and rerun deployment | RD-P1-012; AD018-CON | TC-P1-AD018-OPS-06 |
| Run tables deployed before readiness | RD-P1-020 | TC-P1-AD018-OPS-01 |
| Catalogue remains P2-owned | RD-P1-021 | TC-P1-AD018-OPS-04 |
| No P1 case list | RD-P1-024 | TC-P1-AD018-OPS-04 |
| NFR-067 monitoring and run book | Program BRD | TC-P1-AD018-OPS-05; AC14 |
| NFR-068 failure alert timing (Proposed, DL11) | Program BRD; DL11 | TC-P1-AD018-OPS-05 |
| NFR-015 no ACE operation | Program BRD | TC-P1-AD018-OPS-04 |

### 19. Out of scope

- APP implementation and migration authoring (RWB-P1-AD018-APP).
- Contract publication and provider fake creation (RWB-P1-AD018-CON).
- P2 catalogue ownership and other services' job operations.
- Case list, case-list schedule and case-list alerting (rwb-case; RD-P1-024).
- Cross-service real ACE journey (RWB-ITG-AD018-ITG), the route contract (RWB-PLT-N001-CON) and alerts on outbound files (rwb-integration).

### Remaining delivery steps

- Size: Pending squad refinement; owner delivery lead.
- Epic design sign-off: Pending; owner solution architect.
- CON Done: Pending; owner contract owner.
- Contract fake published at the approved version: Pending; owner contract owner.
- Synthetic test data in DEV: Pending; owner test data owner.