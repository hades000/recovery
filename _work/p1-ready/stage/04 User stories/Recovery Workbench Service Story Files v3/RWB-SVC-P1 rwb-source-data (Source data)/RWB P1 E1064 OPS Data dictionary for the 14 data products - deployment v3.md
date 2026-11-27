# RWB-P1-E1064-OPS Data dictionary for the 14 data products

**Version 3 changes.**
- This release applies no dictionary migration and verifies the RWB-P1-E1001-APP baseline as at least 123 objects and 1,379 fields with every baseline ID (RD-P1-025). Where the 22 November change log below says otherwise, version 3 prevails.
- Delta on the RWB-P1-E1015-OPS chart with a chart-diff check, flag-off 404, flag-first rollback (RD-P1-044, 045).
- Readiness, alert thresholds, flag store, PROD path, smoke run and runbook corrected; AC10 to AC16 added from the review.
- Review findings fixed: 1 to 3, 5 to 12, 14 to 19. Left pending with an owner: 4 and 13.
- Batch D: the runbook order of a release that adds fields is stated: the dictionary load is applied first (RD-P1-071).

**Version and date.** v3, 27 November 2026.

**Change log.** D-RCV-60, 27 November 2026: applied RD-P1-006, RD-P1-025, RD-P1-044 and RD-P1-045, and corrected the cited review findings. Agent: S6-stories.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-064 for rwb-source-data. The single deployment of the monolith becomes the release of the dictionary slice on its own chart, with the `rwb_source_data` sequence applied by its own migration step that refuses any other schema (DP-15), the five tables and their 122 and 1,366 rows (superseded: at least 123 objects and 1,379 fields, RD-P1-025) verified after the migration, the flag `rwb.dataengine.data-dictionary` gating the two controllers, the series and the two alerts of ADR-023 with one runbook entry each, and a smoke run that reads a page of fields, proves the publish refusal and the stale-version refusal, and is rolled back. The dictionary stays P1's in `rwb_source_data` (DP-01) and the 30 `recovery.v_ace_*` views stay in schema `recovery` and are not migrated or created here (DP-05). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1064-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (8 resolved, 21 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

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
| Size | Not specified in the source documents (DOR-RWB-P1-E1064-OPS-16) |
| Patterns applied | DP01, DP05, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P1-N |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1015-OPS and RWB-P1-E1064-APP |
| Depends on (build) | RWB-P1-E1001-APP, RWB-P1-E1015-OPS, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-PLT-N004-OPS, RWB-PLT-E1044-OPS |
| Contract dependencies | RWB-P1-E1064-CON |
| Contract version | 5.1.0 (Recovery Workbench API Specification v7, rwb-source-data.yaml) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-004, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-026, FR-P1-027, FR-P1-029) |
| Readiness decisions | RD-P1-006, RD-P1-020, RD-P1-025, RD-P1-044, RD-P1-045, RD-P1-071 |
| Status | Draft (directive resolutions) |

### 1. Story

As a **deployment owner**, I want **the dictionary slice released with its chart, flag, probes, alerts and runbook**, so that **a release of the five admin operations is repeatable and observable and the E1001 baseline is verified before promotion**.

The slice this release carries is the one of RWB-P1-E1064-APP and RWB-P1-E1064-CON: the five admin operations `GET /admin/data-dictionary/fields`, `PATCH /admin/data-dictionary/fields/{fieldCode}`, `GET /admin/data-contracts`, `PATCH /admin/data-contracts/{contractId}` and `POST /admin/data-contracts/{contractId}/publish` on base `/api/recovery/source-data/v1`, behind gateway-bff. E1001 owns the dictionary baseline; this release verifies it and applies no dictionary migration. It deploys, verifies, gates and observes; it writes no application code, publishes no contract document and creates no table of its own.

### 2. Business rationale

The legacy story assumed one process in one module: the dictionary tables, the five endpoints and the confirmation record sat in the same deployment as every other module of the monolith, so a failed load and a refused publish were rows in the log of the same application that took the call. In the target the dictionary is a service of its own, its five tables live in its own schema, and its callers are a screen through gateway-bff and the reference-data contract of rwb-case (DP-01, DP-07, DP-19; Architecture v5 slides 11, 15, 29 and 41).

That separation is what this story makes operable. A missing baseline object or field, an unconfirmed publish that succeeds, or an update that ignores `If-Match` would break the dictionary contract. This release verifies the RWB-P1-E1001-APP baseline migration history row, every baseline object name and field ID, counts of at least 123 objects and 1,379 fields, and a `sys_field_version` row for every field added by an approved governed load. It also smoke-checks the publish refusal and stale-version refusal.

Observability follows ADR-023 per service and keeps the personal-data rule of the platform: the series and the two alerts carry counts, status codes, message identifiers, environments and build IDs only, never a field value and never a document reference (Architecture v5 slide 11). The deployment also enforces the ownership boundary operationally: the release carries the `rwb_source_data` login only, verifies the `rwb_source_data` baseline only, refuses a verification target in another schema, and creates none of the 30 `recovery.v_ace_*` views (DP-01, DP-02, DP-05, DP-15).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The `rwb_source_data` schema, its login and the per-service Flyway sequence exist, delivered by RWB-PLT-NF06-DB and the baseline of RWB-P1-E1001-APP (DP-02, DP-15).
- RWB-P1-E1015-OPS is the base release: it owns the rwb-source-data chart, the API and worker deployments, the probes, the Flyway migration job and the login secret reference. This story adds values keys and its own objects only and redefines none of them (RD-P1-044). The chart follows RWB-PLT-N004-OPS: 2 API pods, `/health` and `/metrics`.
- RWB-P1-E1001-APP has applied its baseline migration on `rwb_source_data`; this release verifies its migration history and baseline rows, and applies no dictionary migration (RD-P1-025).
- The contract of RWB-P1-E1064-CON is published, so the smoke run can call the five operations with a known shape and a known envelope.
- DEV, SIT and UAT each hold one synthetic unconfirmed DRAFT contract, one synthetic field and a signed-in synthetic user with Reference data U for the smoke run. Their identifiers and the user are Pending, owner QA lead with solution architect (GAP-3471). Neighbouring services are stood in by the fakes of RWB-P1-E1064-CON.
- The platform flag store holds `rwb.dataengine.data-dictionary` with its values for DEV, SIT, UAT and PROD; it is removed in the release after it is on in production. Its named owner and removal date are Pending, owner release owner (GAP-3472).
- The platform secret store holds the `rwb_source_data` credential, and no secret appears in a values file, a chart template, a dashboard or the runbook.
- The observability platform of ADR-023 is in force, so a series can carry the environment, the release and the build ID as dimensions.
- The alert thresholds, windows, probe timings and incident route are not given by any source (GAP-0500; ASM-0692). The replica count, probe path and scrape path are those of RWB-PLT-N004-OPS.

### 4. Flow

1. The pipeline runs the platform template stages of RWB-PLT-N004-OPS (build, unit, component, contract and boundary tests, image and dependency scan, helm lint and template, migration lint and drift check) and publishes one chart version with one image digest.
2. The chart deploys the API deployment of rwb-source-data with the `rwb_source_data` login, the namespace `rwb-recovery`, the base `/api/recovery/source-data/v1` behind gateway-bff, the build ID of the release and the flag value of the environment.
3. The verification step reads only `rwb_source_data`; it fails if pointed at another schema and creates no object. This release runs no dictionary migration.
4. The verification step reads the baseline history row, confirms every baseline object name and field ID, asserts at least 123 `sys_objects` rows and 1,379 `sys_fields` rows, and checks that every post-baseline field has a `sys_field_version` row from an approved governed load.
5. The flag `rwb.dataengine.data-dictionary` is evaluated at run time from the platform flag store; with the flag off the five operations answer 404 and nothing is redeployed (RD-P1-045 item 4).
6. The dashboards are published with the series of section 11 and the environment, release and build ID as dimensions.
7. The alerts are wired to their runbook entries: the publish refusal rate alert carries MSG-P1-021, the field-change conflict rate alert carries MSG-GEN-004, and the latency and 503 alerts of AC12 carry the build ID.
8. The smoke run (DEV, SIT, UAT) calls the deployed service through gateway-bff as the synthetic user: `GET /admin/data-dictionary/fields?size=1`; `POST /admin/data-contracts/{contractId}/publish` on the unconfirmed synthetic contract with a new UUID `Idempotency-Key`, expecting 409 MSG-P1-021; and `PATCH /admin/data-dictionary/fields/{fieldCode}` on the synthetic field with a stale `If-Match` and a reason, expecting 409 MSG-GEN-004. A refused call writes nothing; the run asserts both versions and the contract status unchanged (AC14). PROD runs read-only checks only (AC10).
9. The release is promoted only when the smoke run passes; a failing smoke run leaves the previous build in force.
10. The rollback path is rehearsed: first the flag is switched off; only if the flag does not cover the fault is the previous image tag and chart version redeployed, and the release note names every P1 capability the redeploy reverts. No migration is reversed (RD-P1-045).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the baseline verification fails | The deployment stays unready and the pipeline stops; no traffic is served | None | AC1 |
| X2 | Baseline verification is pointed at a schema other than `rwb_source_data` | The step refuses and records the refused target; no object is created and no table is touched | Pipeline error, no message id | AC3 |
| X3 | Baseline verification finds a missing table, baseline object name or field ID, or fewer than 123 objects or 1,379 fields | The verification step fails the release and names the missing table or item | Pipeline error, no message id | AC3 |
| X4 | The readiness probe answers before the E1001 baseline history row is present, or the liveness probe answers while the process is stuck | The pod is not routed, or is restarted; the release fails its smoke run | None | AC4 |
| X5 | A publish of an unconfirmed contract is accepted, or its refusal is not on the series | The smoke run fails the release; the runbook recovery for the synthetic row is followed; in a running environment the publish refusal rate alert fires only above its threshold | MSG-P1-021 | AC5, AC15 |
| X6 | A field change from a stale version is accepted | The smoke run fails the release; the runbook recovery for the synthetic row is followed; the conflict rate alert fires only above its threshold | MSG-GEN-004 | AC5, AC15 |
| X7 | The flag is off in an environment | The five operations answer 404, no row is written and the pods keep running; the messageCode of the answer is Pending (GAP-3472) | None | AC2 |
| X8 | A new build is promoted while field changes are being written | The previous build drains and the new build takes new requests; both build IDs appear on the series | None | AC1, AC6 |
| X9 | The release is rolled back after a failed smoke run | The previous chart version and digest serve the five operations; no row is lost or duplicated | None | AC8 |

X1 and X2 are the deployment paths; X3 and X4 are the facts the release verifies instead of assuming; X5 and X6 are the two refusals the contract promises and the release proves; X7 is the flag; X8 and X9 are the promotion and the rollback. The thresholds, windows, timings and routes behind them are environment values and are not in the source set (GAP-0500; ASM-0692).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the flag library and the observability platform; no application code is built here |
| Negotiable | Replica counts, resource sizes, probe timings, alert thresholds, windows and the incident route are environment values |
| Valuable | Makes the release repeatable, the baseline check safe against a wrong schema, and the two refusals of the contract visible |
| Estimable | One chart, one baseline verification, one verification step, the series, two alerts and three runbook entries |
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
    When the chart is rendered for DEV, SIT, UAT and PROD
    Then each render succeeds with the chart version and the image digest pinned
    Then the deployment carries the build ID of the release and serves the base /api/recovery/source-data/v1 behind gateway-bff
    Then the release declares the rwb_source_data login and no other service's credential
    Then every deployment value comes from the values file of the environment and none is hard-coded in a template
    Then each render holds 2 API pods with /health and /metrics, and resources, probe timings, log level, flag default, thresholds and windows are values (GAP-0500; ASM-0692)
    Then a rendered chart diff against the RWB-P1-E1015-OPS base release shows no change to an object this story does not own
    When a render or the baseline verification is forced to fail in SIT
    Then the pipeline stops and the previous build keeps all traffic

  Scenario: AC2 The platform flag controls the dictionary operations (new, D-RCV-60)
    Given the flag `rwb.dataengine.data-dictionary` is registered in the platform flag store with its values for DEV, SIT, UAT and PROD
    Given the flag is off in SIT
    When a user with Reference data U calls each of the five operations
    Then each answers 404, no row is written and no deployment occurs
    When the flag is turned on in the platform store
    Then each operation answers and the change is logged with actor, time and reason

  Scenario: AC3 The E1001 baseline is verified without a dictionary migration (new, RD-P1-025)
    Given the migration history of `rwb_source_data` holds the RWB-P1-E1001-APP step `V<seq>__rwb_p1_e1001_data_products.sql`
    When the release verification reads the baseline
    Then every baseline object name and field ID is present; `sys_objects` has at least 123 rows and `sys_fields` at least 1,379 rows
    And every post-baseline field has a `sys_field_version` row from an approved governed load
    When the verification target is not `rwb_source_data`
    Then verification exits non-zero, creates no object and records the target schema in the pipeline log
    And this release applies no dictionary migration

  Scenario: AC4 Readiness follows process start and baseline history (new, D-RCV-60)
    Given the process has not started or the E1001 baseline history row is absent
    When the readiness probe runs
    Then it is not ready
    Given the process has started and the baseline history row is present
    When readiness runs before any user request, including while rwb-case is down
    Then it is ready
    And liveness is healthy while the process is up and its loop is responsive
    And neither probe writes a row or waits for a downstream service
    And the probes are those of RWB-P1-E1015-OPS on /health; this release redefines none of them

  Scenario: AC5 Alerts use rate thresholds, not individual refusals (new, D-RCV-60)
    Given the SIT refusal-rate threshold and window are configured as environment values
    When refusals remain below the threshold
    Then no alert fires
    When the refusal rate exceeds the threshold
    Then one alert of MSG-P1-021 or MSG-GEN-004 includes the message ID, build ID and runbook reference and no field value
    And threshold and window remain Pending under GAP-0500 / ASM-0692, owner platform operations

  Scenario: AC6 The dashboards carry the environment, the release and the build ID (new, D-RCV-60)
    Given the published dashboard of the deployment
    When a synthetic run reads a page of fields and the two refusals are produced
    Then the dashboard shows the field-read rate, the field-read failures by status, the field-change rate, the contract read rate and the publish attempts by result
    Then each series carries the environment, the release and the build ID as labels and no other
    Then one field read, one refused publish and one refused change each raise their series by 1 (metric names and units Pending, GAP-3480)
    Then a refused publish and a refused field change are both visible on the dashboard before any alert is read
    Then no series carries a field value, a document reference or a person

  Scenario: AC7 The runbook covers the three conditions of the slice (new, D-RCV-60)
    Given the runbook of the deployment
    When it is reviewed against the exception paths of section 5
    Then it holds one entry each for failed baseline verification, readiness failure, rollback, a refused publish and a field-change conflict, and one for a smoke call that was accepted
    Then each entry names the check to run, the owner role and the recovery step
    Then the entry for failed baseline verification states that the previous build stays in force and that any baseline correction is owned by RWB-P1-E1001-APP and never edits an applied migration
    Then the entry for a refused publish states that the confirmation is recorded by the data steward and not by the operator
    Then the runbook carries no secret and no personal value

  Scenario: AC8 A rollback keeps the previous build and its data (new, D-RCV-60)
    Given the row counts and latest versions of sys_field_version and data_contract are recorded
    And a release is promoted to SIT and its smoke run passed
    When the flag is switched off
    Then the five operations answer 404 and no row changes
    When the release is rolled back to the previous chart version
    Then neither row count nor latest version is lower
    And the previous build reads the rows written by the new build and serves traffic with its own digest and build ID
    And the rollback changes no schema
```

**Target reading.** The sixteen criteria are new, because the legacy story had no deployment section: it assumed the tables, the five endpoints and the confirmation record sat in one monolith release. What they assert is the split. The baseline is created by RWB-P1-E1001-APP; this release verifies its presence and applies no dictionary migration (RD-P1-025). The chart, probes and migration job are owned by RWB-P1-E1015-OPS and this release is a delta on them (RD-P1-044). The five tables are P1's and no other service's schema is read (DP-01). The 30 `recovery.v_ace_*` views stay in schema `recovery` and are not created, altered or granted by this release (DP-05). The five operations are reached over REST through gateway-bff, one hop, so the deployment registers a route and no direct call (DP-11, DP-19). Thresholds, timings and the incident route are carried as the placeholder (GAP-0500; ASM-0692).

```gherkin
  Scenario: AC9 A failing release leaves the previous build in force until the new build passes its tests and its smoke run (new, D-RCV-60)
    Given a working build in force in SIT and a new build released with no user traffic
    When the new build fails its tests or its smoke run
    Then the previous build stays in force with its own build ID and the new build does not replace it
    Then the new build receives user traffic only after it passes its tests and its smoke run
    Then this release applies no dictionary migration and a baseline defect is corrected by RWB-P1-E1001-APP through a new version

  Scenario: AC10 PROD release and rollback use read-only checks (new, review section E)
    Given the previous tag is serving in PROD
    When the new tag is promoted through the PROD gate and a post-release read-only check fails
    Then the previous tag is redeployed
    And the check made no write call and no schema changed

  Scenario: AC11 The release login cannot create objects outside its schema (new, review section E)
    Given the `rwb_source_data` login used by the release
    When it attempts CREATE in another `rwb_` schema and in `public`
    Then both attempts are denied

  Scenario: AC12 Latency and 503 alerts use the agreed target (new, review section E)
    Given the 2 s response-time target at the 95th percentile in Non Functional Specification v5 section 3.2
    And the SIT alert threshold and window are configured as environment values under GAP-0500 and DL11
    When the latency or 503 rate exceeds its configured threshold
    Then the named alert fires with the build ID and a runbook link

  Scenario: AC13 Telemetry contains no personal value or document reference (new, review section E)
    Given a synthetic contract with confirmation document UUID `00000000-0000-4000-8000-000000006400` and a refused publish
    When the run's logs, traces, series and alert payloads are searched
    Then neither that document reference nor a field value appears

  Scenario: AC14 The smoke run leaves the synthetic rows unchanged (new, review section E)
    Given the versions of the synthetic field and contract are recorded
    When the smoke run completes
    Then both versions and the contract status are unchanged

  Scenario: AC15 A stale-version acceptance fails the release (new, review section E)
    Given a test build accepts a stale If-Match in an isolated synthetic fixture
    When the smoke run executes
    Then the build fails, is not promoted and the runbook recovery for the test row is followed

  Scenario: AC16 Two pods start without applying a dictionary migration (new, RD-P1-025)
    Given the E1001 baseline history row is already present in `rwb_source_data`
    When two pods start at the same time
    Then both observe the baseline and become ready after verification
    And neither applies a dictionary migration nor changes the schema

```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login and one schema per service: the release carries the `rwb_source_data` login, verifies the baseline in `rwb_source_data` only and refuses any other target schema | Architecture v5 slides 11 and 29; DP-02, DP-15 |
| BR2 | The RWB-P1-E1001-APP baseline history row and every baseline object name and field ID are present; counts are at least 123 and 1,379, and every later field has an approved governed-load version row | REQ-RDF-001; legacy RWB-E1-064 BR2, BR8; RD-P1-025 |
| BR3 | A publish without a confirmation is refused with MSG-P1-021 and a change from a stale version is refused with MSG-GEN-004; the release proves both in its smoke run | REQ-RDF-011; legacy RWB-E1-064 BR4, BR5, BR7 |
| BR4 | Every alert carries a message identifier and links one runbook entry | Template and Rules §R7.2 s14; ADR-023 |
| BR5 | No environment value is hard-coded: replicas, resources, probe timings, thresholds, windows, routes and the flag come from the values files of the environment | Template and Rules §R7.2 s17 |
| BR6 | Series and alert payloads carry counts, status codes, message identifiers, environments and build IDs only, never a field value, a document reference or a person | Architecture v5 slide 11 (PDPA); ADR-023 |
| BR7 | The release writes no dictionary row and reads no other service's table; the smoke calls use synthetic records through the five operations and write nothing | DP-01, DP-11 |
| BR8 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run; this release applies no dictionary migration | DP-10, DP-15 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Baseline verification passed | `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` have the E1001 migration history row, all baseline IDs, minimum counts and approved post-baseline versions | Ready |
| Deploying | Baseline verification refused | The target schema is not `rwb_source_data`; no dictionary migration is run | Blocked |
| Deploying | Verification failed | A table, a baseline object name or a field ID is missing, or a count is below its minimum | Blocked |
| Ready | Release superseded | A new chart version passes its tests and its smoke run | Rolling |
| Rolling | All pods on the new build | The previous build drains | Ready |
| Ready | Flag off | `rwb.dataengine.data-dictionary` is turned off in the platform store | Ready, with the five operations answering 404 |
| Ready | Smoke run failed | The read, the publish refusal or the stale-version refusal fails | Blocked |
| Blocked | Previous build restored | The previous chart is redeployed with its own build ID | Ready |

A field version and a data contract have the states of section 9 of RWB-P1-E1064-CON; the states above are states of the deployment and not of a row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Platform team (DevOps) | Owns the values keys of this slice, the pipeline stages, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the secret store, the flag library and the ingress route |
| ACE database administrator | No duty in this release: it grants nothing and applies no migration |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the three runbook entries and opens an incident when a refusal rate persists |
| Data steward and data product owner (RW-DATASTEW) | Records a confirmation the operator may not record, and reads the release record (Reference data U) |
| RW-AUDIT | Reads the release record and the change history of the dictionary |
| RW-PLATADM, platform administrator role | Reads the series, the alerts and the runbook and receives the incident |

The release runs as the `rwb_source_data` service identity (DP-02), carried by the chart as a secret reference and never as a literal credential. No name of a person appears in a values file, a dashboard, an alert or a runbook entry.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, build ID, flag value, alert thresholds, windows and route (GAP-0500; ASM-0692) | BR5 |
| Schema | `rwb_source_data`, created by the E1001 baseline; this release verifies its history and applies no dictionary migration | BR1 |
| Objects verified | E1001 baseline history row; all baseline object names and field IDs; `sys_objects` at least 123 and `sys_fields` at least 1,379; approved post-baseline `sys_field_version` rows | BR2 |
| Objects not created here | The 30 `recovery.v_ace_*` views in schema `recovery`, created by RWB-P1-E1069-APP and reached by this service's own read path (DP-05) | BR7 |
| Platform library objects | `processed_event`, `idempotency_key` and `outbox_event`, created in `rwb_source_data` by the library (DP-09, not in this story's pattern set) | Not specified in the source documents (DOR-RWB-P1-E1064-OPS-7) |
| Series | Field-read rate, field-read failures by status, field-change rate, contract read rate, publish attempts by result, response time of the five operations; labels environment, release, build ID | BR6 |
| Alerts | Publish refusal rate (MSG-P1-021), field-change conflict rate (MSG-GEN-004), latency above 2 s at the 95th percentile, 503 rate, readiness failure | BR3, BR4 |
| Runbook entries | Failed baseline verification, readiness failure, rollback, refused publish, field-change conflict, accepted smoke call; each with the check, owner role and recovery step | BR4 |
| Secrets | This slice adds no secret; the chart keeps its existing secrets, the `rwb_source_data` login among them | BR1 |
| Test data | One synthetic field, one synthetic unconfirmed DRAFT contract and a synthetic user in DEV, SIT and UAT (identifiers Pending, GAP-3471); no production payload and no real document reference | BR7 |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded (GAP-0500; ASM-0692).

**Reference load and ACE read.** The governance rows for `sys_fields` arrive through the rwb-case reference-load operation `POST /api/recovery/case/v1/admin/reference-loads` and are applied by the handler of RWB-P1-E1064-APP (ASM-0531, ASM-0533, ASM-0534). This deployment configures nothing of that path. When one release brings a dictionary load and loads that name its new fields, the dictionary load is applied first (RD-P1-071).

**Reference-table read.** The service reads LOV-ROLE and LOV-REFRESH through `GET /api/recovery/case/v1/admin/lists/{listCode}`; the release configures only the client timeout values.

**Approved governance load.** P3 owns approval state, approver and rollback in `rwb_case.reference_version`. P1 applies an approved version atomically and records the applied version on its rows; this deployment does not create a load-state record or apply a dictionary migration (RD-P1-020).

**Probes.** The probes are owned by RWB-P1-E1015-OPS on `/health`. Readiness needs the process started and the baseline migration history row present; it does not wait for a request or for rwb-case. Liveness is healthy while the process is up and its loop is responsive. Neither probe writes a row. The initial delay and periods are environment values (GAP-0500; ASM-0692).

### 12. Contract

#### 12.1 REST operations provided

None from this story. `GET /api/recovery/source-data/v1/admin/data-dictionary/fields`, `PATCH /api/recovery/source-data/v1/admin/data-dictionary/fields/{fieldCode}`, `GET /api/recovery/source-data/v1/admin/data-contracts`, `PATCH /api/recovery/source-data/v1/admin/data-contracts/{contractId}` and `POST /api/recovery/source-data/v1/admin/data-contracts/{contractId}/publish` are declared by RWB-P1-E1064-CON and implemented by RWB-P1-E1064-APP; this deployment exposes them through the chart and the ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None from the deployment. The baseline verification, the verification step and the smoke run read the catalogue and call the service under test; the chart carries no REST client of its own, no composite route and no outbound call at start-up. The one read of the reference-data contract of rwb-case is a run-time call of the service and is not configured by this release (DP-07).

#### 12.3 Events published

None. The topic `rwb.source-data.events.v1` carries `AceDataReady` and `AceDataLate`, published by RWB-P1-E1015-APP, and this release publishes neither and declares no producer of its own (DP-14).

#### 12.4 Events consumed

None. No consumer group is created by this release; the dictionary slice is called over REST and consumes no topic (Architecture v5 slide 15).

#### 12.5 Workflows and activities

None. The slice is synchronous and this release registers no workflow, activity or worker on the task queue `rwb-source-data` of namespace `rwb-recovery`; the two workflows and the two activities on that queue belong to other P1 stories (Architecture v5 slide 15).

#### 12.6 Schedules

None. The deployment registers no Temporal Schedule and no Quartz job: a dictionary change is a person's admin call and a load is a reference-load call (DP-07; DP-10 is not in this story's pattern set).

#### 12.7 Tables owned

None. This deployment creates no table and owns no object: the five dictionary tables and their baseline are created by RWB-P1-E1001-APP. This release applies no dictionary migration and verifies the E1001 baseline history row, every baseline object name and field ID, at least 123 objects and 1,379 fields, and approved governed-load version rows; the 30 `recovery.v_ace_*` views are RWB-P1-E1069-APP's and are neither created nor granted here (DP-01, DP-05, DP-15). The verification step reads the catalogue and asserts the five tables; it creates nothing and repairs nothing.

#### 12.8 Contract fakes

None is deployed. The smoke run calls the deployed service on synthetic records; neighbouring services are stood in by the fakes of RWB-P1-E1064-CON and RWB-P3-E1043-CON, and the real cross-service proof belongs to RWB-ITG-E1064-ITG.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The five dictionary operations are the app story's; the probes are cluster-internal |
| Kafka | 0 published, 0 consumed | No topic of this service and no consumer group in this release |
| Temporal | 0 workflows, 0 activities, 0 Schedules | No worker on `rwb-source-data` |
| File | None | No file is read or written by the deployment; the load file arrives inside the reference-load request of the rwb-case contract and is never staged |
| SQL | One schema verified, none migrated | The baseline verification of section 11 reads `rwb_source_data` only |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release verifies `rwb_source_data` only and reads no other schema; it applies no dictionary migration | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The 30 views stay in schema `recovery`; the release creates none and grants none | none |
| DP-07 | Reference data, LOV | The rwb-case reference-data contract is a run-time dependency of the load; the deployment configures nothing of it | H RWB-PLT-E1043-CON |
| DP-11 | In-process call, published interface | The five operations are reached over REST through gateway-bff; the smoke run uses the same path | none |
| DP-13 | `/api/recovery/v1` | The ingress serves `/api/recovery/source-data/v1` and no other base | none |
| DP-15 | V0001 baseline, migration | The per-service Flyway history in `rwb_source_data`; this release verifies the E1001 baseline and applies no dictionary migration | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff serves the dictionary and contract screens; the deployment registers the route and no screen of its own | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-source-data/` overlay | Values keys of this slice only: ingress route for the five operations, flag default, build ID and alert values; the deployments, probes and secret references stay those of RWB-P1-E1015-OPS |
| `helm/rwb-source-data/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` and `values-prod.yaml` | Image digest, resources, probe timings, log level, flag default, build ID, alert thresholds and windows (GAP-0500; ASM-0692); the 2 API pods are the platform value |
| Pipeline stage | Platform template build, unit/contract tests, image/dependency scan, chart publish, baseline verification, smoke run and promotion; no dictionary migration step |
| Baseline verification | Confirms E1001 migration history row, baseline IDs, minimum counts, and governed-load version rows; no dictionary migration is applied |
| Verification step | The E1001 baseline history row, baseline object and field IDs, minimum counts of 123 and 1,379, and post-baseline governed-load versions |
| Dashboards | The series of section 11 with the three dimensions |
| Alerts | The rules of section 11, each with a threshold value and one runbook entry |
| Runbook | The entries of section 11 |

**Alert mapping**

| Identifier | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-021 | The publish refusal rate is above its threshold in its window (one correct refusal does not alert) | Publish refusal alert naming the release, the build ID and the status code, with the rate and the window | Platform on-call, page (route and window are environment values: GAP-0500; ASM-0692) |
| MSG-GEN-004 | The field-change conflict rate is above its threshold in its window | Field-change conflict alert naming the release, the build ID and the status code, with the rate and the window | Platform on-call, ticket (route and window are environment values: GAP-0500; ASM-0692) |

**Rollback** (RD-P1-045). (1) Switch `rwb.dataengine.data-dictionary` off. (2) Only if the flag does not cover the fault, redeploy the previous image tag and chart version of rwb-source-data; because the chart is shared, the release note names every P1 capability the redeploy reverts. (3) Never reverse a migration; this release applies none, and a baseline defect is corrected by RWB-P1-E1001-APP through a new forward version. Rows written by the new build stay. The previous tag passes its smoke test against the current schema in the pipeline. The release owner rolls back when the post-deploy checks fail, the platform smoke workflow reports no result for the day or an incident is attributed to the release.

**Feature switch.** `rwb.dataengine.data-dictionary`, in the platform flag store, evaluated at run time. On: the five operations answer through gateway-bff. Off: they answer 404, no row is written, the pods keep running and the rest of the service is unchanged; what the reference-table handler does when off, and the messageCode of the 404, are Pending, owner release owner (GAP-3472). The five tables are not behind a flag.

**Done when.** The chart renders for DEV, SIT, UAT and PROD with a pinned digest and build ID and no change to objects it does not own, verification confirms the baseline in each environment, the series and alerts are published with their runbook links, the smoke run reads a page of fields and gets its two 409 answers without writing, the rollback is rehearsed and the runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-021 | A publish of a contract with no confirmation is refused, and the publish refusal alert fires | The data contract for {system} cannot be published until its system owner confirms it. |
| MSG-GEN-004 | A field change from a stale version, or with no `If-Match` version, is refused, and the conflict alert fires | Someone else changed this record. Reload it to see their change. |

The two texts are the legacy texts of RWB-E1-064, copied unchanged, and they are the two messages the release proves and alerts on. The status code that carries each one (409 for both, and 428 for a missing `If-Match`) is fixed by RWB-P1-E1064-CON and is not restated as a deployment value. The threshold, the window and the route of each alert are not given by any source and are carried as the placeholder (GAP-0500; ASM-0692). An alert payload names counts, status codes, message identifiers, environments and build IDs only, never a field value, a document reference or a person.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard, the alert route and the runbook. The dictionary screen and the contract screen of SCR-40 that reach the five operations are served by the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), and this deployment only registers the route; the screen states are those of section 9 of RWB-P1-E1064-CON and belong to the screen owners; the empty, loading, error and no access states are Not specified in the source documents (CG-ALL-2250). The platform administrator reads the release result and the series under Platform administration R, and internal audit reads the release record and the change history of the dictionary under the same right.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1064-OPS-01 | AC1 | NFR | Renders for DEV, SIT, UAT, PROD; chart diff; forced failure |
| TC-P1-E1064-OPS-02 | AC2 | NFR | Flag off and on in SIT; five operations; change log of the flag |
| TC-P1-E1064-OPS-03 | AC3 | NFR | Baseline verification, a foreign schema target |
| TC-P1-E1064-OPS-04 | AC4 | NFR | Readiness with and without the history row; rwb-case down |
| TC-P1-E1064-OPS-05 | AC5 | NFR | Refusals below and above the SIT threshold |
| TC-P1-E1064-OPS-06 | AC6 | NFR | A synthetic read and the two refusals on the dashboard |
| TC-P1-E1064-OPS-07 | AC7 | NFR | Runbook entries against the exception paths |
| TC-P1-E1064-OPS-08 | AC8 | NFR | Flag off, redeploy of the previous tag, rows compared |
| TC-P1-E1064-OPS-09 | AC9, BR8 | NFR | Failing tests and failing smoke run over a working build |
| TC-P1-E1064-OPS-10 | AC10 | Component | PROD promotion with a failing read-only check |
| TC-P1-E1064-OPS-11 | AC11 | Component | CREATE attempts in another schema and in public |
| TC-P1-E1064-OPS-12 | AC12 | Component | Injected delay and 503 rate in SIT |
| TC-P1-E1064-OPS-13 | AC13 | Component | Search of logs, traces, series and alert payloads |
| TC-P1-E1064-OPS-14 | AC14 | Component | Versions before and after the smoke run |
| TC-P1-E1064-OPS-15 | AC15 | Component | Test build that accepts a stale If-Match |
| TC-P1-E1064-OPS-16 | AC16 | Component | Two pods starting together |
| TC-P1-E1064-APP-11 to TC-P1-E1064-APP-19 | Regression evidence: criteria owned by RWB-P1-E1064-APP | End to end and Component | As listed in RWB-P1-E1064-APP section 16 |

The test case IDs are those of Test Cases v9, tab Story test cases.

### 17. Guardrails

- No business value in a values file: owners, refresh cycles, late behavior and contract content are data rows in `rwb_source_data`, never a deployment value.
- No personal data in logs, series, alert payloads, the runbook or the smoke data: counts, status codes, message identifiers, environments and build IDs only; the smoke rows are synthetic and no production payload is copied into a fixture.
- One login and one schema: the release carries the `rwb_source_data` login, verifies its baseline only and refuses any other target schema (DP-02, DP-15).
- The release creates none of the 30 `recovery.v_ace_*` views, alters none and grants none; they stay in schema `recovery` and only this service reads them (DP-01, DP-05).
- The baseline is verified on every environment and never assumed; a missing table, baseline name or field ID, or a count below its minimum, blocks the release (BR2).
- No secret is written into a values file, a chart template, a dashboard or the runbook; the credential comes from the platform secret store.
- An applied migration is never edited and a published contract is never edited in place; this release applies no dictionary migration (DP-15).
- A failing smoke run never replaces a working build, and a rollback keeps the previous digest and build ID (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner, read from ACE through read-only views and not copied | The baseline verified without a dictionary migration, and the rule that the 30 views are not created here | TC-P1-E1064-OPS-01, TC-P1-E1064-OPS-03 |
| REQ-RDF-011 | Every data product has a catalog entry stating its definition, owner, system of record and refresh | The publish refusal and stale-version smoke calls, and the rollback | TC-P1-E1064-OPS-05, TC-P1-E1064-OPS-08 |
| ADR-023 | Observability per service | The series, the alerts and the runbook entries | TC-P1-E1064-OPS-05, TC-P1-E1064-OPS-06 |
| NFR-020, NFR-027, NFR-064; Non Functional Specification v5 section 3.2 | Response time target, release and cutover, observability | Latency and 503 alerts, PROD path, logs without personal values | TC-P1-E1064-OPS-10, TC-P1-E1064-OPS-12, TC-P1-E1064-OPS-13 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1064-APP | App development | Sibling: the five operations and governed-load behavior this release smoke-checks; no dictionary migration is deployed here |
| RWB-P1-E1064-CON | Contract | Sibling: the document, the five schemas, the envelope and the fixtures the smoke run uses |
| RWB-ITG-E1064-ITG | Integration | Proves the five operations and the reference-table handler against the live rwb-case contract |
| RWB-P1-E1001-APP | App development | Required baseline dependency: the five tables, at least 123 object rows and 1,379 field rows and `v_data_dictionary` |
| RWB-P1-E1015-OPS | DevOps | Required base release: chart, deployments, probes and migration job (RD-P1-044) |
| RWB-P1-E1069-APP, RWB-P1-E1069-DB | App development and ACE DB | Prerequisite: the 30 views, the login and the grants the release does not create |
| RWB-PLT-NF06-DB | ACE DB | Prerequisite: the schema and the login the release runs as |
| RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the reference-data contract, the per-service sequence and the composite route the release is built on |

### 19. Out of scope

- The two controllers, the two services, the handler and the migration as code: RWB-P1-E1064-APP.
- The contract documents, the five schemas, the envelope and the fixtures: RWB-P1-E1064-CON; this story only deploys, verifies and gates them.
- The five tables, their DDL, the baseline seed rows (at least 123 objects and 1,379 fields) and `v_data_dictionary`: RWB-P1-E1001-APP.
- The 30 `recovery.v_ace_*` views, the login, the grants and the four extension tables: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- The reference-data contract of rwb-case and its reference-load operation: RWB-P3-E1043-CON, consumed and not defined here (DP-07).
- The real cross-service proof of the five operations and of the handler against the live rwb-case contract: RWB-ITG-E1064-ITG.
- The dictionary and contract screens of SCR-40 and the gateway-bff composite route: the screen owners and RWB-PLT-N001-CON (DP-19).
- The platform components: the Kafka topics and the schema registry, the Temporal cluster and its namespace, the flag library, the secret store and the observability platform (the platform epics).
- The exact deployment topology, resource sizes, replica counts, probe timings, alert thresholds, windows and the incident route; they are set per environment by the platform team (GAP-0500; ASM-0692).
- Freshness stamps, retention and the reconciliation report of this service: RWB-P1-E1015-APP, RWB-P1-E1017-APP and RWB-P1-E1011-APP.

### 20. Remaining delivery steps

- Size: Not specified; owner delivery squad.
- Epic design sign-off: Pending; owner product owner and solution architect.
- Contract Done (RWB-P1-E1064-CON): Pending; owner contract owner.
- Fake published: Pending; owner contract owner.
- Smoke records and synthetic user (GAP-3471): Pending; owner QA lead.
- Flag owner and removal date (GAP-3472): Pending; owner release owner.
- Alert thresholds, windows and route (GAP-0500, DL11): Pending; owner platform team.
- Synthetic test data in DEV: Pending; owner QA lead.
