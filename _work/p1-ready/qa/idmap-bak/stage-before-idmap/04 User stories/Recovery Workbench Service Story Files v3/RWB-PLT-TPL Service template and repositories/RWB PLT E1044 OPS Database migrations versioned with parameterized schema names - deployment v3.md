# RWB-PLT-E1044-OPS Database migrations versioned with parameterized schema names

**Version 3 changes.**
- D-RCV-60 P1 developer readiness (RD-P1 register). Backfilled 4 mapped v9 test case IDs.
- No job-run record and no rerun through rwb-source-data: the outcome of a migration is the service's own Flyway history and logs; a failure is fixed by a new version and a redeploy (RD-P1-012; findings RWB-PLT-E1044-OPS#1, #2, #6).
- Added the forward-only rollback order, BR9 and AC9 (RD-P1-045; finding #3).
- AC5 and AC8 rewritten; ACE guardrail corrected; header and test rows corrected (findings #4, #5, #7, #8, #9).

**Version and date.** v3, 27 November 2026.

**Change log.** D-RCV-60, 27 November 2026: applied RD-P1-012 and RD-P1-045 and fixed the cited affected-story review findings. D-RCV-60 P1 developer readiness (RD-P1 register). Agent: F09-affected.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1044-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-044 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Size | To be sized by the squad at refinement (DOR-RWB-PLT-E1044-OPS-16) |
| Patterns applied | DP01, DP05, DP06, DP07, DP13, DP14, DP15, DP19 |
| Parallel lane | L-PLT-TPL-H |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-PLT-E1044-CON (In build; not yet Done) |
| Contract version | v1 of the RWB-PLT-E1044-CON migration contract; no rwb-source-data operation is consumed (RD-P1-012) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-005, FR-PLT-006, FR-PLT-007) |
| Readiness decisions | RD-P1-012, RD-P1-045 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: deployment side of RWB-E1-044 for the 19 services: Flyway on service start, the drift gate, the forward-only PROD rule, the key-store account, the job-run record and the two-instance lock (ADR-021; DP-15). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (8 resolved, 20 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer of the platform**, I want **Flyway to run on service start in every environment, one migration run per service, the drift gate before SIT, UAT and PROD, forward-only PROD, the migration account read from the key store as a secret reference, each run's outcome kept in the service's own Flyway history and logs and a two-instance lock**, so that **a deployment applies exactly the pending migrations of that service and stops before an environment whose schema has drifted**.

### 2. Business rationale

The migration rule is only as good as the deployment that runs it. Arch v5 slide 29 puts Flyway in each service's own pipeline; slide 33 deploys every service as two parts (an API deployment and a worker deployment on the same task queue), so two instances of one service can start at the same moment and both would try to migrate. This story fixes the deployment side: the run at start, one run per service, the drift gate before each environment, the forward-only rule in PROD, the account from the key store, the run outcome that is read from the service's own Flyway history and logs and the lock that lets two instances start safely. The legacy feature flag `rwb.p3.migration-drift-gate` keeps its name and its values across the split: on in SIT, UAT and PROD, off in DEV. It supports REQ-RDF-001, REQ-RDF-014 and NFR-052 (the key store).

### 3. Preconditions

- The platform template and the Helm chart deploy a service as an API deployment and a worker deployment (RWB-PLT-TPL; Arch v5 slide 33).
- Each service has its own schema `rwb_<name>`, its own login and its own history table (RWB-PLT-E1044-APP-2; Arch v5 slide 29).
- The migration account of each service and its read-only drift account are entries in the key store (NFR-052).
- No rwb-source-data operation is needed: a migration run is not a P1 job (RD-P1-012).
- The feature flag library of the platform is available to the pipeline and the chart.
- No build dependency: the story has no build dependency and is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Pipeline: build and test the service image; the migration files are inside the image.
2. Pipeline: run the drift gate before the deployment to SIT, UAT and PROD: apply the migrations to a clean container and compare the object list with the target schema through the read-only account.
3. Pipeline: stop the deployment when the gate finds a difference and the flag is on; report only in DEV where the flag is off.
4. Deployment: on service start, Flyway reads its account from the key store, applies each pending migration of that service once in version order and writes the checksum to the service's own history table.
5. Deployment: the second instance that starts at the same moment waits for the Flyway lock, finds nothing pending and starts.
6. Deployment: the outcome of the run is the service's own history table `flyway_schema_history` (version, checksum, installed time, success) and the pipeline and service start logs. No job record is written to rwb-source-data (RD-P1-012).
7. Platform administrator or DevOps engineer: reads the outcome from that history and the logs, with the service, the schema, the version, the checksum and the drift result of the pipeline stage.
8. DevOps engineer: after a failed migration, merges the fix as a new version and redeploys; the next start applies it. There is no rerun operation for a migration.
9. Release owner: to roll back, first switches the change's feature flag off; only if the flag does not cover the fault, redeploys the previous image tag and chart version. A migration is never reversed (RD-P1-045).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The drift gate finds an object that the migrations do not produce | The deployment stops before it starts and the object is named | MSG-P3-016 | AC2 |
| X2 | An applied migration file was edited | Flyway validation fails, the pod does not become ready and the deployment stops | MSG-P3-016 | AC1 |
| X3 | A pipeline step calls Flyway clean or an undo file is present in PROD | The step is refused and no object changes | MSG-P3-016 | AC3 |
| X4 | The migration account cannot be read from the key store | The pod does not start; the failure is logged without the secret | None | AC4 |
| X5 | Withdrawn (RD-P1-012): no job-run record is written | None | None | Not applicable |
| X6 | A migration fails part way | The transaction rolls back, the history holds no successful row for the version, the pod does not become ready and the start log names the version | MSG-P3-016 | AC1, AC5 |
| X7 | Two instances of one service start together | One applies the migrations, the other waits for the lock and finds nothing pending | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the template, the chart and the per-service schema and login |
| Negotiable | The gate wiring and the alert threshold are settled with the platform team; the rules are fixed |
| Valuable | A deployment can never change a schema by hand or leave an environment drifted |
| Estimable | The gate stage, the start configuration, the rollback proof and the lock test |
| Small | Fits one sprint with its tests |
| Testable | Each criterion runs in a pipeline against containers and a two-instance environment |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of per-service migrations

  Background:
    Given each service has its own schema rwb_<name>, its own login and its own history table
    Given the migration account of each service is a secret reference in the key store

  Scenario: AC1 Start applies pending migrations once (new, D-RCV-60)
    Given a service with two pending migrations in SIT
    When the service starts
    Then both migrate in version order and the history records them with their checksums
    When the service starts a second time
    Then no migration runs and no object changes

  Scenario: AC2 The drift gate runs before each deployment (new, D-RCV-60)
    Given the feature flag rwb.p3.migration-drift-gate is on in SIT, UAT and PROD and off in DEV
    When a column has been added by hand to the service's schema
    Then the gate fails with MSG-P3-016, names the object and stops the deployment in SIT, UAT and PROD
    Then in DEV the gate reports the same difference and the deployment continues

  Scenario: AC3 PROD refuses clean and undo (new, D-RCV-60)
    Given the PROD profile
    When a pipeline step calls Flyway clean or an undo file is present
    Then the step is refused with MSG-P3-016
    Then no object in PROD changes

  Scenario: AC4 The migration account is a secret reference (new, D-RCV-60)
    Given the migration account of each service in the key store
    When the pipeline and the pod read it
    Then the account is a secret reference and never a value in a pipeline file, an image, a log or a prompt
    Then a scan of the pipeline files, the chart and the image finds no credential

  Scenario: AC5 Each run's outcome is in the service's own history and log (RD-P1-012)
    Given a service start in SIT with one pending migration
    When the migration succeeds
    Then flyway_schema_history of that service holds one row for the version with its checksum, installed_on time and success true
    Then no request is sent to GET /api/recovery/source-data/v1/admin/jobs and no job record is written
    When the next pending migration fails
    Then the history holds no successful row for it, the pod does not become ready and the start log carries MSG-P3-016 naming the version

  Scenario: AC6 Two instances start together (new, D-RCV-60)
    Given two instances of one service starting at the same moment with one migration pending
    When both start
    Then one applies the migration and the other waits for the lock and finds nothing pending
    Then both instances start and the connections of the login stay within its PgBouncer cap

  Scenario: AC7 Each business rule has a criterion and a test case (new, D-RCV-60)
    Given the business rules BR1 to BR9 in section 8
    When the criteria in section 7 and the test cases in section 16 are read
    Then each rule BR1 to BR9 is covered by at least one criterion and one test case

  Scenario: AC8 A failed key store call stops the run (RD-P1-012)
    Given a service start in SIT where the key store does not answer
    When the migration run needs the migration account
    Then the run applies no migration and flyway_schema_history is unchanged
    Then the pod does not become ready and the failure is logged without the secret
    Then one failed-run alert is raised for the service

  Scenario: AC9 Rollback never reverses a migration (new, RD-P1-045)
    Given a release applied in SIT whose migrations only add objects
    When the release owner switches the change's flag off and the fault remains
    Then the previous image tag and chart version are deployed and pass their smoke test against the migrated schema
    Then no migration is reversed, no U*.sql or down script runs and the history rows stay
    Then the fault in a migration is corrected only by a new forward version

```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Flyway runs on service start in every environment and applies each pending migration of that service once | RWB-E1-044 flow step 5; DP-15 |
| BR2 | One migration run per service; a run of one service never applies the migrations of another service | ADR-021; Arch v5 slide 29 |
| BR3 | The drift gate runs before every deployment to SIT, UAT and PROD and stops it on a difference | RWB-E1-044 BR7 |
| BR4 | PROD runs forward only: clean is disabled and an undo file is refused; a fix is a new version | RWB-E1-044 BR4 |
| BR5 | The migration account and the read-only drift account are secret references from the key store; no credential appears in a pipeline file, an image, a log or a prompt | NFR-052; RWB-E1-044 precondition 3 |
| BR6 | The outcome of each run is the service's own `flyway_schema_history` and its logs; no job record is written to rwb-source-data and a migration is not listed or rerun through `/admin/jobs` | RD-P1-012 rule 2; DP-15 |
| BR7 | Two instances of one service may start together: the Flyway lock lets one apply and the other wait and start | RWB-E1-044 AC9 |
| BR8 | The feature flag `rwb.p3.migration-drift-gate` keeps its name and values: on in SIT, UAT and PROD, off in DEV, where drift is reported and the deployment continues | RWB-E1-044 feature flag |
| BR9 | Rollback order: flag off first; previous image tag and chart version only if the flag does not cover the fault; a migration is never reversed. Every migration of a release works with the previous tag (expand only). The release owner rolls back when post-deploy checks fail, the platform smoke workflow (JOB-22) reports no result for the day, or an incident is attributed to the release | RD-P1-045 items 1, 2 and 6 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Deployment starts | The drift gate passes, or the flag is off in DEV | Migrating |
| Migrating | All pending versions applied | The history records every checksum | Complete |
| Migrating | A version fails | A statement fails, or validation fails | Failed (rolled back, the pod does not become ready) |
| Failed | Fix merged and the service is redeployed | The fix is a new version | Migrating |
| Complete | Second instance starts | The lock is released and nothing is pending | Complete |
| Complete | Drift gate fails before the next deployment | An object is not produced by the migrations | Deployment stopped |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Runs deployments and redeploys after a fix (no rerun operation); reads the run outcome from the history and logs |
| RW-DATASTEW, data steward | Platform administration R. Pending: how this role reads migration runs, owner Solution architect (NEW-GAP-F09-1) |
| RW-AUDIT, internal audit | Platform administration R. Pending: how this role reads migration runs, owner Solution architect (NEW-GAP-F09-1) |
| DevOps engineer of the platform | Owns the pipeline stage, the gate wiring, the chart values and the flag entry |
| Pipeline migration account of the service | Applies the migrations of that service with that service's login from the key store |
| Key store administrator | Owns the secret entries and their rotation; not a Workbench role |

### 11. Data

No business field. The deployment writes no job-run record. The run outcome is read from the service's own `flyway_schema_history` (Flyway columns, among them version, checksum, installed_on and success); the drift result is the output of the pipeline stage. It reads the migration account from the key store and the object list of the service's own schema from `information_schema`.

| Field | Where it is read |
|---|---|
| service | Deployment pipeline run |
| schema | Chart value `RWB_SCHEMA` |
| version | `flyway_schema_history.version` |
| checksum | `flyway_schema_history.checksum` |
| drift result | Drift gate stage output |
| run time | `flyway_schema_history.installed_on` and the pipeline run times |
| outcome | `flyway_schema_history.success` for an applied version; the start log for a failed one |

No job-run record is written (RD-P1-012); the deployment raises one alert per failed run per service; the feature flag `rwb.p3.migration-drift-gate` is owned by the platform library owner with its legacy values unchanged (GAP-1423).

### 12. Contract

#### 12.1 REST operations provided

None. The deployment provides no REST operation.

#### 12.2 REST operations consumed

None. A migration run is not an rwb-source-data job: neither `GET /admin/jobs` nor `POST /admin/jobs/{jobId}/rerun` is called (RD-P1-012).

#### 12.3 Events published

None. A migration run publishes no event.

#### 12.4 Events consumed

None. A migration run consumes no event.

#### 12.5 Workflows and activities

None. The run is a deployment step in the Flyway module, not a Temporal workflow or activity.

#### 12.6 Schedules

None. There is no schedule; the run is triggered by service start and by the pipeline step.

#### 12.7 Tables owned

None. The deployment owns no business table; Flyway writes `flyway_schema_history` inside the service's own schema.

#### 12.8 Contract fakes

None. No job view fake of rwb-source-data is used (RD-P1-012).

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None | No rwb-source-data operation is consumed |
| Kafka | None | No event is published or consumed |
| Temporal | None | The run is not a workflow |
| File | None | The migration files are read from the image of the service |

### 13. Solution plan

**Deliverables.** The golden pipeline stage that runs the drift gate before SIT, UAT and PROD, the chart values that read the migration account from the key store and set `RWB_SCHEMA` per environment, the start configuration with `spring.flyway.clean-disabled=true` and the lock, the rollback proof against the previous tag and the flag entry of `rwb.p3.migration-drift-gate`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read ACE data through rwb-source-data's contract only; only rwb-source-data reads `recovery.v_ace_*` (D-RCV-60) | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. Add the drift gate stage to the golden pipeline before SIT, UAT and PROD; wire the flag so a difference stops the deployment when the flag is on.
2. Set the chart values for `RWB_SCHEMA` per environment and point the migration account and the read-only account at their key-store references.
3. Set the start configuration: validation on start, out-of-order off, clean disabled in every profile and the lock on.
4. Prove the previous image tag passes its smoke test against the migrated schema (RD-P1-045) and that a failed migration is recovered by a new version and a redeploy.
5. Prove two instances start together: one applies, the other waits and both become ready.
6. Prove the DEV behaviour: the flag is off and a difference is reported while the deployment continues.
7. Prove the scan: no credential in a pipeline file, the chart, the image or a log.

**Done when.** The test cases of section 16 pass in SIT, the gate stops a drifted SIT/UAT/PROD deployment and passes it in DEV, PROD refuses clean and undo, and two instances start together inside the connection cap.

The alert threshold and the owner of the feature flag after the split are Not specified in the source documents (GAP-1423; ASM-2491); a single failed-run alert and the platform library as the flag owner are used until the point is closed. The job-run record part of GAP-1423 no longer applies to this story (RD-P1-012).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-016 | Drift found, checksum mismatch, a refused clean or undo, or a failed migration | Schema check failed in {schema}: {object}. The deployment was stopped. |
| MSG-P4-002 | A role without Platform administration R reads the migration runs. Not raised by this story while no operation serves migration runs (NEW-GAP-F09-1) | You cannot {action} here. Your role does not include it. |

MSG-P3-016 is the message of RWB-E1-044, carried unchanged; it is shown in the pipeline log and the start log, not to business users.

### 15. Screens and states

No new screen. SCR-44 Interface and job monitor receives no migration run from `GET /admin/jobs` and offers no rerun of a migration (RD-P1-012). Pending: whether SCR-44 shows migration runs and through which read, owner Solution architect (NEW-GAP-F09-1). The flag `rwb.p3.migration-drift-gate` has two states per environment: blocking in SIT, UAT and PROD, report only in DEV. Empty, loading, error and no access states: Not specified in the source documents (CG-ALL-1516).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1044-OPS-01 | AC1, BR1, BR2 | Component | A service with two pending migrations; start applies once, the second start changes nothing |
| TC-PLT-E1044-OPS-02 | AC2, BR3, BR8 | End to end | A hand-added column in SIT, UAT and PROD stops the deployment; the same in DEV only reports |
| TC-PLT-E1044-OPS-03 | AC3, BR4 | Component | PROD profile with a clean call and an undo file; both refused, no object changes |
| TC-PLT-E1044-OPS-04 | AC4, BR5 | NFR | Scan of the pipeline files, the chart, the image and the logs; no credential, account is a secret reference |
| TC-PLT-E1044-OPS-05 | AC5, BR6 | End to end | One successful and one failed migration read from the service's own history and start log; no call to rwb-source-data. |
| TC-PLT-E1044-OPS-06 | AC6, BR7 | NFR | Two instances starting together, inside the PgBouncer cap of the login, both ready |
| TC-PLT-E1044-OPS-07 | AC7, BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 | Component | Each rule in section 8 checked against the criteria in section 7 and the test cases in section 16; each has at least one of each |
| TC-PLT-E1044-OPS-08 | AC8, BR6 | Component | Key store does not answer at service start; no migration, history unchanged, pod not ready, one alert. |
| TC-PLT-E1044-OPS-09 | AC9 | End to end | AC9 Rollback never reverses a migration (new, RD-P1-045) |

The rows TC-PLT-E1044-OPS-01 to TC-PLT-E1044-OPS-08 are not yet in Recovery Workbench Test Cases v8; they are to be added in Test Cases v9 (W2-tests).

### 17. Guardrails

- One schema and one login per service: the run uses the login of the service and touches no other schema (DP-01, DP-02).
- No credential in a pipeline file, a chart value, an image layer, a log or a prompt; every account is a secret reference from the key store.
- No drift gate bypass in PROD: the flag is on in SIT, UAT and PROD and only DEV reports instead of blocking.
- Forward only in PROD: no clean, no undo file, no manual change; a fix is a new version through the pipeline.
- No business value in a migration and no personal data in a migration, a test or a log.
- ACE data only through the P1 rwb-source-data contract; only rwb-source-data reads `recovery.v_ace_*` (D-RCV-60).
- One migration run per service; a run never applies the migrations of another service.
- The two-instance lock stays on in every environment; a lock bypass is a defect.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | Recovery data held in 14 data products in the ACE database | The run at service start writes the objects of the service's own schema | TC-PLT-E1044-OPS-01, TC-PLT-E1044-OPS-05 |
| REQ-RDF-014 | Stage 2 data products exist before the first treatment goes live | The gate and the run order guarantee the schema before the service serves traffic | TC-PLT-E1044-OPS-01, TC-PLT-E1044-OPS-02 |
| NFR-052 | Database and drift accounts held in the key store | The chart reads the accounts as secret references; the scan proves no credential | TC-PLT-E1044-OPS-04 |
| ADR-021 | Per-service Flyway and migration ownership | One run per service, forward only in PROD, the lock and the history of the run | TC-PLT-E1044-OPS-03, TC-PLT-E1044-OPS-06 |

Open decisions DL34 (ASM-0193) and DL35 (ASM-0189, ASM-0377, ASM-2041, ASM-2051): the directive confirms each assumption, and the recommended resolution applies.

### 19. Out of scope

- The migration contract document and its fixtures (RWB-PLT-E1044-CON).
- The Flyway module wiring and the per-service baselines (RWB-PLT-E1044-APP-2).
- The as-built monolith behaviour, kept word for word in RWB-PLT-E1044-APP.
- The creation of the 19 schemas and logins and the grants (RWB-PLT-NF06-DB).
- The platform dashboards and alerts beyond the one failed-run alert (RWB-PLT-OBS).
- Deployment slots and release windows (DL34, DL35).

## Remaining delivery steps

- Size the story at refinement (squad).
- Sign the epic design for RWB-PLT-TPL (Solution architect).
- Bring RWB-PLT-E1044-CON to Done at a pinned version, without the job view run record (platform library owner).
- Add TC-PLT-E1044-OPS-01 to -08 and the rollback case in Test Cases v9 (test lead).
- Create the synthetic migration fixtures and the key-store entries in DEV and SIT (DevOps team).
- Rule where migration runs are read (Solution architect, NEW-GAP-F09-1).
