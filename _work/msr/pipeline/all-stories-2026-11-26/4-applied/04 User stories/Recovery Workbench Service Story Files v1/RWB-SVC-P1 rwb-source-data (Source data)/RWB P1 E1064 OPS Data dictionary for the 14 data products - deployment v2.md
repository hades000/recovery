# RWB-P1-E1064-OPS Data dictionary for the 14 data products

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-064 for rwb-source-data. The single deployment of the monolith becomes the release of the dictionary slice on its own chart, with the `rwb_source_data` sequence applied by its own migration step that refuses any other schema (DP-15), the five tables and their 122 and 1,366 rows verified after the migration, the flag `rwb.dataengine.data-dictionary` gating the two controllers, the series and the two alerts of ADR-023 with one runbook entry each, and a smoke run that reads a page of fields, proves the publish refusal and the stale-version refusal, and is rolled back. The dictionary stays P1's in `rwb_source_data` (DP-01) and the 30 `recovery.v_ace_*` views stay in schema `recovery` and are not migrated or created here (DP-05). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-E1064-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P1-E1064-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-064 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P1-N |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-004, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-026, FR-P1-027, FR-P1-029) |
| Status | Draft (realignment v1) |

### 1. Story

As a **DevOps engineer**, I want **the dictionary slice deployed with its chart, its flag, its migration step, its probes, its alerts and its runbook**, so that **a release of the five admin operations is repeatable and observable and a failed migration is refused before it touches `rwb_source_data`**.

The slice this release carries is the one of RWB-P1-E1064-APP and RWB-P1-E1064-CON: the five admin operations `GET /admin/data-dictionary/fields`, `PATCH /admin/data-dictionary/fields/{fieldCode}`, `GET /admin/data-contracts`, `PATCH /admin/data-contracts/{contractId}` and `POST /admin/data-contracts/{contractId}/publish` on base `/api/recovery/source-data/v1`, behind gateway-bff, with the five tables of the dictionary verified after every migration. It deploys, verifies, gates and observes; it writes no application code, publishes no contract document and creates no table of its own.

### 2. Business rationale

The legacy story assumed one process in one module: the dictionary tables, the five endpoints and the confirmation record sat in the same deployment as every other module of the monolith, so a failed load and a refused publish were rows in the log of the same application that took the call. In the target the dictionary is a service of its own, its five tables live in its own schema, and its callers are a screen through gateway-bff and the reference-data contract of rwb-case (DP-01, DP-07, DP-19; Architecture v5 slides 11, 15, 29 and 41).

That separation is what this story makes operable. A migration that runs against the wrong schema, a table that is missing after a deploy, a publish that silently succeeds on an unconfirmed contract, or a field change that overwrites a colleague's version are conditions that no unit test of the service can see, and each of them breaks the one promise of the dictionary: one published definition per field. The release therefore verifies four things on every environment instead of trusting the migration once: that the migration step refused every target schema but `rwb_source_data`, that the five tables and their 122 and 1,366 rows are present after the migration, that a publish without a confirmation is refused with MSG-P1-021, and that a change from a stale version is refused with MSG-GEN-004.

Observability follows ADR-023 per service and keeps the personal-data rule of the platform: the series and the two alerts carry counts, status codes, message identifiers, environments and build IDs only, never a field value and never a document reference (Architecture v5 slide 11). The deployment also enforces the ownership boundary operationally: the release carries the `rwb_source_data` login only, applies the `rwb_source_data` migration only, refuses any other target schema, and creates none of the 30 `recovery.v_ace_*` views (DP-01, DP-02, DP-05, DP-15).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The `rwb_source_data` schema, its login and the per-service Flyway sequence exist, delivered by RWB-PLT-NF06-DB and the baseline of RWB-P1-E1001-APP (DP-02, DP-15).
- The chart of rwb-source-data and its values files exist from the earlier P1 releases, with base `/api/recovery/source-data/v1` and the ingress served by gateway-bff (DP-13, DP-19).
- The dictionary migration of RWB-P1-E1064-APP is merged on the service sequence, and its version is the one this release applies; the module and its migration ship together.
- The contract of RWB-P1-E1064-CON is published, so the smoke run can call the five operations with a known shape and a known envelope.
- The dictionary fixture, the contract fixture and the reference-data fake of that contract are available in the service environment, so the smoke run exercises the five operations without calling a live rwb-case.
- The flag library is in force and the flag `rwb.dataengine.data-dictionary` is registered for the three environments.
- The platform secret store holds the `rwb_source_data` credential, and no secret appears in a values file, a chart template, a dashboard or the runbook.
- The observability platform of ADR-023 is in force, so a series can carry the environment, the release and the build ID as dimensions.
- The deployment values, the alert thresholds, the probe timings and the incident route are not given by any source: no values file, threshold, timing or routing rule for the dictionary slice exists in the source set (GAP-0500; ASM-0692).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version with one image digest.
2. The chart deploys the API deployment of rwb-source-data with the `rwb_source_data` login, the namespace `rwb-recovery`, the base `/api/recovery/source-data/v1` behind gateway-bff, the build ID of the release and the flag value of the environment.
3. The migration step applies the `rwb_source_data` sequence of this release, the dictionary version included, and refuses to run when the target schema is not `rwb_source_data`; a refused target is recorded and no object is created.
4. The verification step reads the catalogue and asserts the five tables of 11: `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract`, and reads the row counts 122 and 1,366.
5. The flag step sets `rwb.dataengine.data-dictionary` from the values of the environment; with the flag off the two controllers are not deployed and no operation of the slice answers.
6. The dashboards are published with the series of section 11 and the environment, release and build ID as dimensions.
7. The two alerts are wired to their message identifiers and to their runbook entries: the publish refusal alert carries MSG-P1-021 and the field-change conflict alert carries MSG-GEN-004.
8. The smoke run reads one page of fields with `page` and `size`, attempts a publish of a contract with no confirmation against the contract fixture and expects 409 with MSG-P1-021, then sends a field change from a stale `If-Match` version and expects 409 with MSG-GEN-004; both attempts are rolled back.
9. The release is promoted only when the smoke run passes; a failing smoke run leaves the previous build in force.
10. The rollback path is rehearsed: the previous chart version with its own image digest and build ID serves the five operations, and the rows the new build wrote stay, because a field version is never overwritten and a published contract is never edited in place.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The deployment stays unready and the pipeline stops; no traffic is served | None | AC1 |
| X2 | The migration step is pointed at a schema other than `rwb_source_data` | The step refuses and records the refused target; no object is created and no table is touched | Pipeline error, no message id | AC3 |
| X3 | The migration ran but one of the five tables is missing, or the row counts are not 122 and 1,366 | The verification step fails the release and names the missing table or the count | Pipeline error, no message id | AC3 |
| X4 | The readiness probe answers before the migration is applied, or the liveness probe answers while the process is stuck | The pod is not routed, or is restarted; the release fails its smoke run | None | AC4 |
| X5 | A publish of an unconfirmed contract is accepted, or its refusal is not on the series | The smoke run fails the release, and the publish refusal alert fires when the condition recurs in an environment | MSG-P1-021 | AC5 |
| X6 | A field change from a stale version is accepted | The smoke run fails the release, and the field-change conflict alert fires when the condition recurs in an environment | MSG-GEN-004 | AC5 |
| X7 | The flag is off in an environment | The two controllers are not deployed, the five operations answer as refused at the edge and no series is emitted | None | AC2 |
| X8 | A new build is promoted while field changes are being written | The previous build drains and the new build takes new requests; both build IDs appear on the series | None | AC1, AC6 |
| X9 | The release is rolled back after a failed smoke run | The previous chart version and digest serve the five operations; no row is lost or duplicated | None | AC8 |

X1 and X2 are the deployment paths; X3 and X4 are the facts the release verifies instead of assuming; X5 and X6 are the two refusals the contract promises and the release proves; X7 is the flag; X8 and X9 are the promotion and the rollback. The thresholds, windows, timings and routes behind them are environment values and are not in the source set (GAP-0500; ASM-0692).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the flag library and the observability platform; no application code is built here |
| Negotiable | Replica counts, resource sizes, probe timings, alert thresholds, windows and the incident route are environment values |
| Valuable | Makes the release repeatable, the migration safe against a wrong schema, and the two refusals of the contract visible |
| Estimable | One chart, one migration step, one verification step, the series, two alerts and three runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the catalogue shows the five tables, an alert fires on a synthetic metric, the smoke run gets its 409 |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the data dictionary slice for rwb-source-data

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the schema of this service is rwb_source_data
    Given the target environment is SIT

  Scenario: AC1 The slice is deployed from one chart with one digest and one build ID (new, D-RCV-60)
    Given the rwb-source-data chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the deployment carries the build ID of the release and serves the base /api/recovery/source-data/v1 behind gateway-bff
    Then the release declares the rwb_source_data login and no other service's credential
    Then every deployment value comes from the values file of the environment and none is hard-coded in a template
    Then the chart exposes replicas, resources, probe timings, log level, flag value, thresholds and windows as values (GAP-0500; ASM-0692)

  Scenario: AC2 The flag turns the dictionary slice on and off (new, D-RCV-60)
    Given the flag rwb.dataengine.data-dictionary and its values for the three environments
    When the flag is on
    Then the two controllers are deployed and the five operations answer
    When the flag is off in an environment
    Then the two controllers are not deployed in that environment, the five operations are refused at the edge and no series of the slice is emitted
    Then the flag value comes from the values file of the environment and is never hard-coded in a template

  Scenario: AC3 The migration step refuses any schema but rwb_source_data and the five tables are verified (new, D-RCV-60)
    Given the migration step of this release
    When it is pointed at a schema other than rwb_source_data
    Then the step refuses, records the refused target and creates no object
    When it is applied to rwb_source_data in SIT
    Then the catalogue shows the five tables of the baseline: sys_objects, sys_fields, sys_field_version, data_product and data_contract
    Then sys_objects holds 122 rows and sys_fields holds 1,366 rows
    When the migration is applied a second time
    Then Flyway reports the version as already applied and no object, column or key changes

  Scenario: AC4 The readiness and liveness probes answer only when the slice can serve (new, D-RCV-60)
    Given the deployed pod and its two probes
    When the migration has not yet been applied on rwb_source_data
    Then the readiness probe answers not ready and the pod is not routed
    When the migration has been applied and the API has served one request
    Then the readiness probe answers healthy
    Then the liveness probe answers healthy while the process is up and its loop is responsive
    Then neither probe writes a row and neither commits a transaction
    Then a failing dependency is reported as not ready, never as live and broken
    Then the probe paths and timings are environment values (GAP-0500; ASM-0692)

  Scenario: AC5 The publish refusal and the field-change conflict each raise their alert (new, D-RCV-60)
    Given the published alert rules and the runbook
    When a publish of a contract with no confirmation is refused, and a field change from a stale version is refused
    Then the publish refusal alert fires with MSG-P1-021 and the build ID
    Then the field-change conflict alert fires with MSG-GEN-004 and the build ID
    Then neither alert carries a field value, a document reference or a person
    Then every alert links one runbook entry with the check, the owner role and the recovery step
    Then no alert threshold, window or route is hard-coded in a chart template (GAP-0500; ASM-0692)

  Scenario: AC6 The dashboards carry the environment, the release and the build ID (new, D-RCV-60)
    Given the published dashboard of the deployment
    When a synthetic run reads a page of fields and the two refusals are produced
    Then the dashboard shows the field-read rate, the field-read failures by status, the field-change rate, the contract read rate and the publish attempts by result
    Then each series carries the environment, the release and the build ID as dimensions
    Then a refused publish and a refused field change are both visible on the dashboard before any alert is read
    Then no series carries a field value, a document reference or a person

  Scenario: AC7 The runbook covers the three conditions of the slice (new, D-RCV-60)
    Given the runbook of the deployment
    When it is reviewed against the exception paths of section 5
    Then it holds one entry for a failed migration, one for a refused publish and one for a field-change conflict
    Then each entry names the check to run, the owner role and the recovery step
    Then the entry for a failed migration states that the previous build stays in force and that an applied migration is corrected by a new version, never by editing one
    Then the entry for a refused publish states that the confirmation is recorded by the data steward and not by the operator
    Then the runbook carries no secret and no personal value

  Scenario: AC8 A rollback keeps the previous build and loses no row (new, D-RCV-60)
    Given a release promoted to SIT and its smoke run passed
    When the release is rolled back to the previous chart version
    Then the previous build serves the five operations with its own build ID
    Then the rows the new build wrote stay, and no field version is overwritten and no published contract is edited
    Then both build IDs appear on the series while the two builds overlap
    Then the rollback keeps the previous image digest and changes no schema
```

**Target reading.** The eight criteria are new, because the legacy story had no deployment section: it assumed the tables, the five endpoints and the confirmation record sat in one monolith release. What they assert is the split. The migration is the dictionary version of RWB-P1-E1064-APP on this service's own sequence, applied by a step that refuses any schema but `rwb_source_data` (DP-15; Architecture v5 slides 11 and 29). The five tables are P1's and no other service's schema is migrated or read (DP-01). The 30 `recovery.v_ace_*` views stay in schema `recovery` and are not created, altered or granted by this release (DP-05). The five operations are reached over REST through gateway-bff, one hop, so the deployment registers a route and no direct call (DP-11, DP-19). The values, thresholds, timings and the incident route are not given by any source and are carried as the placeholder (GAP-0500; ASM-0692).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login, one schema and one sequence per service: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only and refuses any other target schema | Architecture v5 slides 11 and 29; DP-02, DP-15 |
| BR2 | The five tables of the dictionary and their 122 and 1,366 rows are verified after every migration, on every environment, and a missing table or a wrong count fails the release | REQ-RDF-001; legacy RWB-E1-064 BR2, BR8 |
| BR3 | A publish without a confirmation is refused with MSG-P1-021 and a change from a stale version is refused with MSG-GEN-004; the release proves both in its smoke run | REQ-RDF-011; legacy RWB-E1-064 BR4, BR5, BR7 |
| BR4 | Every alert carries a message identifier and links one runbook entry | Template and Rules §R7.2 s14; ADR-023 |
| BR5 | No environment value is hard-coded: replicas, resources, probe timings, thresholds, windows, routes and the flag come from the values files of the environment | Template and Rules §R7.2 s17 |
| BR6 | Series and alert payloads carry counts, status codes, message identifiers, environments and build IDs only, never a field value, a document reference or a person | Architecture v5 slide 11 (PDPA); ADR-023 |
| BR7 | The release writes no dictionary row of its own and reads no other service's table; the smoke entries are synthetic and go through the five operations against the contract fixtures | DP-01, DP-11 |
| BR8 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run, and an applied migration is corrected by a new version | DP-10, DP-15 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Migration applied and the five tables verified | `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` are present with 122 and 1,366 rows | Ready |
| Deploying | Migration refused | The target schema is not `rwb_source_data` | Blocked |
| Deploying | Verification failed | A table is missing or a count is wrong | Blocked |
| Ready | Release superseded | A new chart version passes its tests and its smoke run | Rolling |
| Rolling | All pods on the new build | The previous build drains | Ready |
| Ready | Flag off | `rwb.dataengine.data-dictionary` is turned off in the environment | Not deployed |
| Ready | Smoke run failed | The read, the publish refusal or the stale-version refusal fails | Blocked |
| Blocked | Previous build restored | The previous chart is redeployed with its own build ID | Ready |

A field version and a data contract have the states of section 9 of RWB-P1-E1064-CON; the states above are states of the deployment and not of a row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the secret store, the flag library and the ingress route |
| ACE database administrator | Grants the five tables to the `rwb_source_data` login and confirms the migration ran on the right schema |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the three runbook entries and opens an incident when a refusal rate persists |
| Data steward and data product owner (RW-DATASTEW) | Records a confirmation the operator may not record, and reads the release record (Reference data U) |
| RW-AUDIT | Reads the release record and the change history of the dictionary |
| RW-PLATADM, platform administrator role | Reads the series, the alerts and the runbook and receives the incident |

The release runs as the `rwb_source_data` service identity (DP-02), carried by the chart as a secret reference and never as a literal credential. No name of a person appears in a values file, a dashboard, an alert or a runbook entry.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, build ID, flag value, alert thresholds, windows and route (GAP-0500; ASM-0692) |
| Schema | `rwb_source_data`, migrated by its own per-service Flyway sequence; this release applies the dictionary version |
| Objects verified after the migration | `sys_objects` (122 rows), `sys_fields` (1,366 rows), `sys_field_version`, `data_product` and `data_contract`, all in `rwb_source_data` |
| Objects not created here | The 30 `recovery.v_ace_*` views in schema `recovery`, created by RWB-P1-E1069-APP and reached by this service's own read path (DP-05) |
| Platform library objects | `processed_event`, `idempotency_key` and `outbox_event`, created in `rwb_source_data` by the library (DP-09, not in this story's pattern set) |
| Series | Field-read rate, field-read failures by status, field-change rate, contract read rate, publish attempts by result; dimensions environment, release, build ID |
| Alerts | The publish refusal with MSG-P1-021; the field-change conflict with MSG-GEN-004 |
| Runbook entries | Failed migration, refused publish, field-change conflict; each with the check, the owner role and the recovery step |
| Secrets | The `rwb_source_data` credential, from the platform secret store; no other credential is carried |
| Test data | Synthetic fields and one synthetic contract from the fixtures of RWB-P1-E1064-CON, read and refused in DEV and SIT; no production payload and no real document reference is used |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded (GAP-0500; ASM-0692).

**Probes.** Readiness answers healthy only after the dictionary migration has been applied on `rwb_source_data` and the API has served one request; liveness answers healthy when the process is up and its loop is responsive. Neither probe reads a field row, writes a version and commits a transaction. A failing dependency is reported as not ready, never as live-and-broken. The probe paths, the initial delay and the periods are environment values (GAP-0500; ASM-0692).

### 12. Contract

#### 12.1 REST operations provided

None from this story. `GET /api/recovery/source-data/v1/admin/data-dictionary/fields`, `PATCH /api/recovery/source-data/v1/admin/data-dictionary/fields/{fieldCode}`, `GET /api/recovery/source-data/v1/admin/data-contracts`, `PATCH /api/recovery/source-data/v1/admin/data-contracts/{contractId}` and `POST /api/recovery/source-data/v1/admin/data-contracts/{contractId}/publish` are declared by RWB-P1-E1064-CON and implemented by RWB-P1-E1064-APP; this deployment exposes them through the chart and the ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None from the deployment. The migration step, the verification step and the smoke run read the catalogue and call the service under test; the chart carries no REST client of its own, no composite route and no outbound call at start-up. The one read of the reference-data contract of rwb-case is a run-time call of the service and is not configured by this release (DP-07).

#### 12.3 Events published

None. The topic `rwb.source-data.events.v1` carries `AceDataReady` and `AceDataLate`, published by RWB-P1-E1015-APP, and this release publishes neither and declares no producer of its own (DP-14).

#### 12.4 Events consumed

None. No consumer group is created by this release; the dictionary slice is called over REST and consumes no topic (Architecture v5 slide 15).

#### 12.5 Workflows and activities

None. The slice is synchronous and this release registers no workflow, activity or worker on the task queue `rwb-source-data` of namespace `rwb-recovery`; the two workflows and the two activities on that queue belong to other P1 stories (Architecture v5 slide 15).

#### 12.6 Schedules

None. The deployment registers no Temporal Schedule and no Quartz job: a dictionary change is a person's admin call and a load is a reference-load call (DP-07; DP-10 is not in this story's pattern set).

#### 12.7 Tables owned

None. This deployment creates no table and owns no object: the five tables of the dictionary are created by the baseline of RWB-P1-E1001-APP, and this release applies the dictionary version of that sequence and verifies the five tables and their 122 and 1,366 rows; the 30 `recovery.v_ace_*` views are RWB-P1-E1069-APP's and are neither created nor granted here (DP-01, DP-05, DP-15). The verification step reads the catalogue and asserts the five tables; it creates nothing and repairs nothing.

#### 12.8 Contract fakes

None is deployed. The dictionary fixture, the contract fixture and the reference-data fake of RWB-P1-E1064-CON run in the service environment and the smoke run calls the five operations against them; the real cross-service proof belongs to RWB-ITG-E1064-ITG.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The five dictionary operations are the app story's; the probes are cluster-internal |
| Kafka | 0 published, 0 consumed | No topic of this service and no consumer group in this release |
| Temporal | 0 workflows, 0 activities, 0 Schedules | No worker on `rwb-source-data` |
| File | None | No file is read or written by the deployment; the load file arrives inside the reference-load request of the rwb-case contract and is never staged |
| SQL | One schema migrated, five tables verified | `rwb_source_data`; the five objects and the row counts of section 11 |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release migrates `rwb_source_data` only and reads no other schema | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The 30 views stay in schema `recovery`; the release creates none and grants none | none |
| DP-07 | Reference data, LOV | The rwb-case reference-data contract is a run-time dependency of the load; the deployment configures nothing of it | H RWB-PLT-E1043-CON |
| DP-11 | In-process call, published interface | The five operations are reached over REST through gateway-bff; the smoke run uses the same path | none |
| DP-13 | `/api/recovery/v1` | The ingress serves `/api/recovery/source-data/v1` and no other base | none |
| DP-15 | V0001 baseline, migration | The per-service Flyway sequence of `rwb_source_data`; the migration step refuses another schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff serves the dictionary and contract screens; the deployment registers the route and no screen of its own | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-source-data/` overlay | API deployment, config map, secret references, probes, ingress route for the five operations, namespace and build ID |
| `helm/rwb-source-data/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, build ID, alert thresholds and windows (GAP-0500; ASM-0692) |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration step, verification step, smoke run, promotion |
| Migration step | The `rwb_source_data` migration of this release, the dictionary version included; a target schema other than `rwb_source_data` is refused |
| Verification step | The catalogue check of the five tables and the row counts 122 and 1,366, and the repeated-run check |
| Dashboards | The series of section 11 with the three dimensions |
| Alerts | Two rules, each with its message identifier and one runbook entry |
| Runbook | Three entries: failed migration, refused publish, field-change conflict |

**Alert mapping**

| Identifier | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-021 | A publish of a contract with no confirmation is refused, or the publish refusal rate is past its threshold | Publish refusal alert naming the release, the build ID and the status code, with the rate and the window | Platform on-call, page (route and window are environment values: GAP-0500; ASM-0692) |
| MSG-GEN-004 | A field change from a stale version, or with no `If-Match` version, is refused, or the conflict rate is past its threshold | Field-change conflict alert naming the release, the build ID and the status code, with the rate and the window | Platform on-call, ticket (route and window are environment values: GAP-0500; ASM-0692) |

**Rollback.** A release that fails the smoke run is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own image digest and build ID; the rows written by the new build stay, because a field version is never overwritten and a published contract is never edited in place. The migration is forward only: a wrong dictionary version is corrected by a new version and never by editing an applied one (DP-15). The series show both build IDs while the two builds overlap, so a refusal is attributable to one of them.

**Feature switch.** `rwb.dataengine.data-dictionary`, from the platform flag library. On: the two controllers are deployed and the five operations answer through gateway-bff. Off: the two controllers are not deployed in that environment, the five operations are refused at the edge, no series of the slice is emitted, and the rest of the service is unchanged. The five tables are not behind a flag.

**Done when.** The chart renders for DEV, SIT and UAT with a pinned digest and the build ID, the migration step refuses a foreign schema, the verification step finds the five tables and the 122 and 1,366 rows in each environment, a repeated migration changes nothing, the series and the two alerts are published with their message identifiers and their runbook links, the smoke run reads a page of fields and gets its two 409 answers with MSG-P1-021 and MSG-GEN-004, the rollback is rehearsed, and the three runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-021 | A publish of a contract with no confirmation is refused, and the publish refusal alert fires | The data contract for {system} cannot be published until its confirming role records the confirmation. |
| MSG-GEN-004 | A field change from a stale version, or with no `If-Match` version, is refused, and the conflict alert fires | Someone else changed this record. Reload it to see their change. |

The two texts are the legacy texts of RWB-E1-064, copied unchanged, and they are the two messages the release proves and alerts on. The status code that carries each one (409 for both, and 428 for a missing `If-Match`) is fixed by RWB-P1-E1064-CON and is not restated as a deployment value. The threshold, the window and the route of each alert are not given by any source and are carried as the placeholder (GAP-0500; ASM-0692). An alert payload names counts, status codes, message identifiers, environments and build IDs only, never a field value, a document reference or a person.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard, the alert route and the runbook. The dictionary screen and the contract screen of SCR-40 that reach the five operations are served by the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), and this deployment only registers the route; the screen states are those of section 9 of RWB-P1-E1064-CON and belong to the screen owners. The platform administrator reads the release result and the series under Platform administration R, and internal audit reads the release record and the change history of the dictionary under the same right.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1064-OPS-01 | AC1 | NFR | The chart rendered for three environments with a pinned digest, the build ID, the `rwb_source_data` login reference and the route; one value moved out of the values file |
| TC-P1-E1064-OPS-02 | AC2 | NFR | The flag on and off in two environments; the values file is the only source of the value |
| TC-P1-E1064-OPS-03 | AC3 | NFR | The migration pointed at a foreign schema and refused; the catalogue after the migration with the five tables and the 122 and 1,366 rows; a repeated run that changes nothing |
| TC-P1-E1064-OPS-04 | AC4 | NFR | The readiness probe before and after the migration; the liveness probe with the process up and with its loop stalled |
| TC-P1-E1064-OPS-05 | AC5 | NFR | A refused publish and a refused field change raise their two alerts, each with one runbook entry and no hard-coded threshold |
| TC-P1-E1064-OPS-06 | AC6 | NFR | A synthetic read and the two refusals; the series carry the three dimensions and no field value |
| TC-P1-E1064-OPS-07 | AC7 | NFR | The three runbook entries reviewed against the exception paths; one entry with a missing owner role |
| TC-P1-E1064-OPS-08 | AC8 | NFR | One release promoted, then rolled back to the previous chart version and digest; the rows of the new build checked as still present |
| TC-E1-064-01 | AC1, BR1, BR2 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Seeded 122 objects and 1,366 fields; count and completeness queries |
| TC-E1-064-02 | AC2, BR2 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | 30 views, 304 fields; one view column with no dictionary row |
| TC-E1-064-03 | AC3, BR1, BR3 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Account ACC0000017 with delay_days 95; dictionary query for DF-ACE-018 |
| TC-E1-064-04 | AC4, BR6, BR9 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Dictionary fixture without DF-ACE-204; load with the correct and the wrong ACE column |
| TC-E1-064-05 | AC5, BR5 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Change of DF-ACE-018 late behavior with a reason and with an empty reason |
| TC-E1-064-06 | AC6, BR4 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | DC-ACE with 304 fields; confirmation on 2026-11-12; a second contract with no confirmation |
| TC-E1-064-07 | AC7 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Two changes to DF-ACE-020 from version 1; one change with no If-Match |
| TC-E1-064-08 | AC8, BR7 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Published DC-ACE and a change to DF-ACE-018 |
| TC-E1-064-09 | Access — regression evidence: the access path belongs to RWB-P1-E1064-APP and rwb-access | Component | RW-TRIBE sends PATCH /admin/data-dictionary/fields/DF-ACE-018; refused with MSG-P4-002 |

The eight deployment cases are this story's and run against the artefacts of a release. The nine legacy cases are carried as regression evidence: their IDs, Covers and Data are kept in legacy order and character for character, the legacy Covers text is qualified as regression evidence, the legacy level "System" maps to "End to end" and "Access" to "Component", and the criteria themselves are owned by RWB-P1-E1064-APP. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in a values file: owners, refresh cycles, late behavior and contract content are data rows in `rwb_source_data`, never a deployment value.
- No personal data in logs, series, alert payloads, the runbook or the smoke data: counts, status codes, message identifiers, environments and build IDs only; the smoke rows are synthetic and no production payload is copied into a fixture.
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only and refuses any other target schema (DP-02, DP-15).
- The release creates none of the 30 `recovery.v_ace_*` views, alters none and grants none; they stay in schema `recovery` and only this service reads them (DP-01, DP-05).
- The five tables are verified on every environment and never assumed; a missing table or a wrong count blocks the release (BR2).
- No secret is written into a values file, a chart template, a dashboard or the runbook; the credential comes from the platform secret store.
- An applied migration is never edited and a published contract is never edited in place: a wrong dictionary version is corrected by a new version (DP-15).
- A failing smoke run never replaces a working build, and a rollback keeps the previous digest and build ID (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner, read from ACE through read-only views and not copied | The `rwb_source_data` migration, the five tables verified after it, and the rule that the 30 views are not created here | TC-P1-E1064-OPS-01, TC-P1-E1064-OPS-03 |
| REQ-RDF-011 | Every data product has a catalog entry stating its definition, owner, system of record and refresh | The contract versioning rule the release proves, the publish refusal alert and the smoke run of the two refusals | TC-P1-E1064-OPS-05, TC-P1-E1064-OPS-08 |
| ADR-023 | Observability per service | The series, the two alerts and the three runbook entries | TC-P1-E1064-OPS-05, TC-P1-E1064-OPS-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1064-APP | App development | Sibling: the five operations and the dictionary migration this release deploys and verifies |
| RWB-P1-E1064-CON | Contract | Sibling: the document, the five schemas, the envelope and the fixtures the smoke run uses |
| RWB-ITG-E1064-ITG | Integration | Proves the five operations and the reference-table handler against the live rwb-case contract |
| RWB-P1-E1001-APP | App development | Prerequisite: the baseline that created the five tables, the 122 and 1,366 rows and `v_data_dictionary` |
| RWB-P1-E1069-APP, RWB-P1-E1069-DB | App development and ACE DB | Prerequisite: the 30 views, the login and the grants the release does not create |
| RWB-PLT-NF06-DB | ACE DB | Prerequisite: the schema and the login the release runs as |
| RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the reference-data contract, the per-service sequence and the composite route the release is built on |

### 19. Out of scope

- The two controllers, the two services, the handler and the migration as code: RWB-P1-E1064-APP.
- The contract documents, the five schemas, the envelope and the fixtures: RWB-P1-E1064-CON; this story only deploys, verifies and gates them.
- The five tables, their DDL, the 122 and 1,366 seed rows and `v_data_dictionary`: RWB-P1-E1001-APP.
- The 30 `recovery.v_ace_*` views, the login, the grants and the four extension tables: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- The reference-data contract of rwb-case and its reference-load operation: RWB-P3-E1043-CON, consumed and not defined here (DP-07).
- The real cross-service proof of the five operations and of the handler against the live rwb-case contract: RWB-ITG-E1064-ITG.
- The dictionary and contract screens of SCR-40 and the gateway-bff composite route: the screen owners and RWB-PLT-N001-CON (DP-19).
- The platform components: the Kafka topics and the schema registry, the Temporal cluster and its namespace, the flag library, the secret store and the observability platform (the platform epics).
- The exact deployment topology, resource sizes, replica counts, probe timings, alert thresholds, windows and the incident route; they are set per environment by the platform team (GAP-0500; ASM-0692).
- Freshness stamps, retention and the reconciliation report of this service: RWB-P1-E1015-APP, RWB-P1-E1017-APP and RWB-P1-E1011-APP.
