# RWB-P1-E1066-OPS Interaction ledger store and writer

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1066-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-066 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P1-Q |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | /v1 path; the exact contract version is not specified in the source documents (DOR-RWB-P1-E1066-OPS-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-029, FR-P1-030) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-066 for rwb-source-data. The single deployment of the monolith becomes the release of the ledger writer on its own chart, with the `rwb_source_data` sequence applied by its own migration step (DP-15), the ledger table, its two unique keys and its append-only trigger verified after the migration, the flag `rwb.dataengine.ledger-writer` gating the writer, five series and three alerts with one runbook entry each (ADR-023), and a smoke run that appends one synthetic entry and replays the same key. The ledger itself stays P1's table in `rwb_source_data` (DP-01, DP-18; the R-PREC default ruling) and no other service's schema is migrated or read. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1066-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (7 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the ledger writer of rwb-source-data deployed from one chart on DEV, SIT and UAT with a pinned image digest and build ID, the `rwb_source_data` migration applied by its own step, the ledger table verified with its columns, its two unique keys, its append-only trigger and its index, the flag `rwb.dataengine.ledger-writer` to turn the writer on and off, five dashboard series, three alerts each with one runbook entry, and a smoke run that appends one synthetic entry and replays the same key without writing a second row**, so that **an operator can see the append rate and its failures, prove that a repeated key writes nothing, and roll back to the previous build without losing or duplicating an entry**.

### 2. Business rationale

The legacy story assumed one process in one module: the ledger table, the writer and the incident hook were in the same deployment, so a failed append was a row in the log of the same application that took the call. In the target the writer is a service of its own, its table lives in its own schema, and the callers are a screen through gateway-bff and an event path of rwb-integration (DP-01, DP-11, DP-19; Architecture v5 slides 11, 29 and 41).

That separation is what this story makes operable. A table that is created by the wrong schema, an append-only trigger that is missing after a migration, a `case_seq` sequence with a gap because a second pod allocated the same number, or an append that fails silently in one environment are all conditions that no unit test of the writer can see, and each of them breaks the one promise of the ledger: the history has no gap. The release therefore verifies four things on every environment instead of trusting the migration once: that the ledger columns and both unique keys exist, that the append-only trigger is present and refuses an update, that a repeated `Idempotency-Key` returns the same entry and the same `caseSeq`, and that an append failure is visible on a series and raises its alert with MSG-P1-022.

Observability follows ADR-023 per service and keeps the personal-data rule of the platform: five series and three alerts carry counts, classes, codes and build IDs only, never a summary and never a contact point (Architecture v5 slide 11). The deployment also enforces the ownership boundary operationally: the release carries the `rwb_source_data` login only, applies the `rwb_source_data` migration only, and refuses any other target schema (DP-01, DP-02, DP-15).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The `rwb_source_data` schema, its login and the per-service Flyway sequence exist, delivered by RWB-PLT-NF06-DB and the baseline of RWB-P1-E1001-APP (DP-02, DP-15).
- The chart of rwb-source-data and its values files exist from the earlier P1 releases, with base `/api/recovery/source-data/v1` and the ingress served by gateway-bff (DP-13, DP-19).
- The ledger migration of RWB-P1-E1066-APP is merged on the service sequence, and its version is the one this release applies; the writer and the migration ship together.
- The contract of RWB-P1-E1066-CON is published, so the smoke run can call `POST /interactions` and `GET /interactions/{entryId}` with a known shape.
- The case fake and the decision-log fake of the contract are available in the service environment, so a smoke run appends a synthetic entry without calling a live rwb-case or rwb-decision.
- The flag library is in force and the flag `rwb.dataengine.ledger-writer` is registered for the three environments.
- The platform secret store holds the `rwb_source_data` credential, and no secret appears in a values file, a chart template, a dashboard or the runbook.
- The observability platform of ADR-023 is in force, so a series can carry the environment, the release and the build ID as dimensions.
- The deployment values, the alert thresholds, the probe timings and the incident route are not given by any source: no values file, threshold, timing or routing rule for the ledger writer exists in the source set (GAP-0506; ASM-0698).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version with one image digest.
2. The chart deploys the API deployment of rwb-source-data with the `rwb_source_data` login, the namespace `rwb-recovery`, the base `/api/recovery/source-data/v1` behind gateway-bff, the build ID of the release and the flag value of the environment.
3. The migration step applies the `rwb_source_data` sequence of this release, ledger version included, and refuses to run when the target schema is not `rwb_source_data`.
4. The verification step reads the catalogue and asserts the ledger objects of 13: the eight ledger columns, the nullable `channel` and `direction`, the unique key `(case_id, case_seq)`, the unique key `(idempotency_key)`, the append-only trigger `tr_interaction_append_only` and the index `ix_interaction_case_time`.
5. The trigger step attempts one `UPDATE` and one `DELETE` on a synthetic row inside a transaction it rolls back, and fails the release when either statement succeeds.
6. The flag step sets `rwb.dataengine.ledger-writer` from the values of the environment.
7. The dashboards are published with the five series of section 11 and the environment, release and build ID as dimensions.
8. The three alerts are wired to their message identifiers and to their runbook entries: the append failure alert carries MSG-P1-022, the incident alert carries the incident code `LEDGER_WRITE_FAILED`, and the trigger alert names the missing object.
9. The smoke run appends one synthetic entry for a synthetic case against the case fake in DEV, reads it back, re-sends the same `Idempotency-Key` and confirms the same entry and the same `caseSeq`, then rolls the transaction of the update attempt back and records the result.
10. The release is promoted only when the smoke run passes; a failing smoke run leaves the previous build in force.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The deployment stays unready and the pipeline stops; no traffic is served | None | AC1 |
| X2 | The migration step is pointed at a schema other than `rwb_source_data` | The step refuses and records the refused target; no object is created | Pipeline error, no message id | AC1 |
| X3 | The migration ran but a ledger column, a unique key, the trigger or the index is missing | The verification step fails the release and names the missing object | Pipeline error, no message id | AC3 |
| X4 | The append-only trigger is missing, or an `UPDATE` or `DELETE` succeeds on a ledger row | The trigger step fails the release and the trigger alert fires | MSG-P1-022 is not used here; the alert carries no message ID and names the object (GAP-0506; ASM-0698) | AC5 |
| X5 | The append fails, or its rate passes the threshold | The failure series rises by class and the append failure alert fires with MSG-P1-022 and the build ID | MSG-P1-022 | AC4, AC5 |
| X6 | The flag is off in an environment | The writer is not deployed, the append answers as refused at the edge and no entry is written | None | AC2 |
| X7 | The smoke run replays the same key and a second row appears | The smoke run fails the release and names the case, the key and the two `caseSeq` values | Pipeline error, no message id | AC6 |
| X8 | A new build is promoted while entries are being appended | The previous build drains and the new build takes new requests; both build IDs appear on the series | None | AC1, AC4 |

X1 and X2 are the deployment paths; X3 and X4 are the four facts the release verifies instead of assuming; X5 and X8 are the observability paths of ADR-023; X6 is the flag; X7 is the one assertion that proves the idempotency of the append in a live environment.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the flag library and the observability platform; no application code is built here |
| Negotiable | Replica counts, resource sizes, probe timings, alert thresholds and the incident route are environment values |
| Valuable | Makes the append rate, its failures, its duplicates and its sequence gaps visible, and makes a rollback safe |
| Estimable | One chart, one migration step, one verification step, one trigger step, five series, three alerts and three runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the catalogue shows the objects, an alert fires on a synthetic metric, the smoke run replays a key |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the interaction ledger writer for rwb-source-data

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the schema of this service is rwb_source_data
    Given the target environment is SIT

  Scenario: AC1 The writer is deployed from one chart with one digest and one build ID (new, D-RCV-60)
    Given the rwb-source-data chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the deployment carries the build ID of the release and serves the base /api/recovery/source-data/v1 behind gateway-bff
    Then the release declares the rwb_source_data login and no other service's credential
    Then the migration step applies the rwb_source_data sequence and refuses a target schema other than rwb_source_data
    Then the migration carries the ledger columns, the append-only trigger and the two unique keys of the interaction table

  Scenario: AC2 The flag turns the writer on and off (new, D-RCV-60)
    Given the flag rwb.dataengine.ledger-writer and its values for the three environments
    When the flag is on
    Then the writer is deployed and the append operation answers
    When the flag is off in an environment
    Then the writer is not deployed in that environment, no entry is written and no append series is emitted
    Then the flag value comes from the values file of the environment and is never hard-coded in a template

  Scenario: AC3 The ledger objects exist after the migration and a repeated run changes nothing (new, D-RCV-60)
    Given the migration of this release has been applied in SIT
    When the catalogue is read for the interaction table
    Then the columns event_code, actor_type, actor_ref, source_ref, idempotency_key, case_seq, decision_log_id and corrects_entry_id exist
    Then channel and direction are nullable
    Then the unique key on (case_id, case_seq) and the unique key on (idempotency_key) exist
    Then the trigger tr_interaction_append_only exists and is enabled
    Then the index ix_interaction_case_time on (case_id, occurred_at) exists
    When the migration is applied a second time
    Then Flyway reports the version as already applied and no object, column, key or trigger changes

  Scenario: AC4 The five series carry the environment, the release and the build ID (new, D-RCV-60)
    Given the published dashboard of the deployment
    When a synthetic run, a set of failed appends and a duplicate key are produced
    Then the dashboard shows the append rate, the append failures by error class, the duplicate hits, the p95 latency of the append and the case_seq gaps
    Then each series carries the environment, the release and the build ID as dimensions
    Then a failed append and a case_seq gap are both visible on the dashboard before any alert is read
    Then no series carries a summary, a contact point or a case identifier beyond the case ID

  Scenario: AC5 The three alerts each link one runbook entry (new, D-RCV-60)
    Given the published alert rules and the runbook
    When a failing append, a raised incident and a dropped trigger are simulated
    Then the append failure alert fires with MSG-P1-022 and the build ID
    Then the incident alert fires on the incident code LEDGER_WRITE_FAILED with the case ID and the error class and no summary
    Then the trigger alert fires when tr_interaction_append_only is missing or disabled, and names the object
    Then every alert links one runbook entry with the check, the owner role and the recovery step
    Then no alert threshold, window or route is hard-coded in a chart template

  Scenario: AC6 The smoke run appends, replays and rolls back cleanly (new, D-RCV-60)
    Given the deployed writer in DEV and the case fake of the contract
    When the smoke run appends one synthetic entry for a synthetic case with a fresh Idempotency-Key
    Then the answer is 201 with the stored entry and its caseSeq
    When the same key is sent again with the same body
    Then the answer carries the same entry ID and the same caseSeq and the table still holds one row
    When the release is rolled back to the previous chart version
    Then the previous build serves the append with its own build ID and no entry is lost or duplicated
```

**Target reading.** The six criteria are new, because the legacy story had no deployment section: it assumed the table, the writer and the incident hook sat in one monolith release. What they assert is the split. The migration is the ledger version of RWB-P1-E1066-APP on this service's own sequence, applied by a step that refuses any schema but `rwb_source_data` (DP-15; Architecture v5 slides 11 and 29). The table is P1's and no other service's schema is migrated or read (DP-01, DP-18). The append is reached over REST through gateway-bff and one hop, so the deployment registers a route and no direct call (DP-11, DP-19). The values, thresholds, timings and the incident route below are not given by any source and are carried as the placeholder (GAP-0506; ASM-0698).

Scenario: AC9 A failing release never replaces a working build: the previous build stays in force until the new build passes its tests and its smoke run (new, D-RCV-60)
  Given a previous build is in force
  When the new build fails its tests or its smoke run
  Then the new build does not replace the previous build
  And the previous build stays in force

Scenario: AC10 A status change the model does not allow is refused (new, D-RCV-60)
  Given a record whose status is governed by the status model (statuses: Not specified in the source documents (NEWAC-RWB-P1-E1066-OPS-AC10))
  When a status change the model does not allow is requested
  Then the change is refused

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login, one schema and one sequence per service: the release carries the `rwb_source_data` login and migrates `rwb_source_data` only | Architecture v5 slides 11 and 29; DP-02, DP-15 |
| BR2 | The ledger table, its two unique keys and its append-only trigger are verified after every migration, on every environment, and a missing object fails the release | REQ-ILG-001; R-UNI-24; legacy RWB-E1-066 BR4 |
| BR3 | A repeated `Idempotency-Key` writes no second row and returns the same entry and the same `caseSeq` | REQ-ILG-007; DP-09; Architecture v5 slide 11 |
| BR4 | Every alert carries a message ID or a named incident code and links one runbook entry | Template and Rules §R7.2 s14; ADR-023 |
| BR5 | No environment value is hard-coded: replicas, resources, probe timings, thresholds, windows and the flag come from the values files of the environment; the deployment values, thresholds, windows and route are Not specified in the source documents (GAP-0506) | Template and Rules §R7.2 s17; GAP-0506 |
| BR6 | Series and alert payloads carry counts, classes, codes, case IDs and build IDs only, never a summary, a contact point or an amount | Architecture v5 slide 11 (PDPA); ADR-023 |
| BR7 | The release writes no entry of its own and reads no other service's table: the smoke entry is synthetic and goes through the append with the case fake | DP-01; DP-18 |
| BR8 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run | DP-15; covered by AC9 and TC-P1-E1066-OPS-08 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Migration applied and the ledger objects verified | The eight columns, the two keys, the trigger and the index are present | Ready |
| Deploying | Verification failed | A column, a key, the trigger or the index is missing | Blocked |
| Ready | Release superseded | A new chart version passes its tests and its smoke run | Rolling |
| Rolling | All pods on the new build | The previous build drains | Ready |
| Ready | Flag off | `rwb.dataengine.ledger-writer` is turned off in the environment | Not deployed |
| Ready | Smoke run failed | The append, the replay or the rollback step fails | Blocked |
| Blocked | Previous build restored | The previous chart is redeployed with its own build ID | Ready |

The ledger entry has no status and is never changed; the states above are states of the deployment and not of a row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the secret store, the flag library and the ingress route |
| ACE database administrator | Grants the ledger objects to the `rwb_source_data` login and confirms the migration ran on the right schema |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the three runbook entries and opens an incident when the append failure rate or a `case_seq` gap persists |
| RW-AUDIT | Reads the append history and the release record |
| RW-PLATADM, platform administrator role | Reads the series, the alerts and the runbook and receives the incident |

The release runs as the `rwb_source_data` service identity (DP-02), carried by the chart as a secret reference and never as a literal credential.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, build ID, flag value, alert thresholds, windows and route (GAP-0506; ASM-0698) | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Schema | `rwb_source_data`, migrated by its own per-service Flyway sequence; this release applies the ledger version | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Ledger objects | The `interaction` table with `event_code`, `actor_type`, `actor_ref`, `source_ref`, `idempotency_key`, `case_seq`, `decision_log_id` and `corrects_entry_id`, a nullable `channel` and `direction`, the unique keys `(case_id, case_seq)` and `(idempotency_key)`, the trigger `tr_interaction_append_only` and the index `ix_interaction_case_time` | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Platform library objects | `processed_event`, `idempotency_key` and `outbox_event`, created in `rwb_source_data` by the library (DP-09) | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Series | Append rate, append failures by error class, duplicate hits, p95 latency of the append, `case_seq` gaps; dimensions environment, release, build ID | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Alerts | Append failure rate with MSG-P1-022; the incident `LEDGER_WRITE_FAILED` with the case ID and the error class; a missing or disabled `tr_interaction_append_only` | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Runbook entries | Append failure, ledger incident, missing trigger; each with the check, the owner role and the recovery step | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Secrets | The `rwb_source_data` credential, from the platform secret store; no other credential is carried | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Test data | One synthetic entry for a synthetic case in DEV, appended against the case fake with a fresh `Idempotency-Key`, and the same key replayed; no production payload is used | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded (GAP-0506; ASM-0698).

**Probes.** Readiness answers healthy only after the migration has been applied on `rwb_source_data` and the API has served one request; liveness answers healthy when the process is up and its loop is responsive. Neither probe writes a ledger row and neither commits a transaction. A failing dependency is reported as not ready, never as live-and-broken.

### 12. Contract

#### 12.1 REST operations provided

None from this story. `POST /api/recovery/source-data/v1/interactions` and `GET /api/recovery/source-data/v1/interactions/{entryId}` are declared by RWB-P1-E1066-CON and implemented by RWB-P1-E1066-APP, and the list read `GET /api/recovery/source-data/v1/interactions` is implemented by RWB-P1-E1068-APP; this deployment exposes them through the chart and the ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None from the deployment. The migration step, the verification step, the trigger step and the smoke run read the catalogue and call the service under test; the chart carries no REST client of its own, no composite route and no outbound call at start-up.

#### 12.3 Events published

None. The topic `rwb.source-data.events.v1` carries `AceDataReady` and `AceDataLate`, published by RWB-P1-E1013-APP, and this release publishes neither. `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library through the outbox when an entry is appended (DP-03, DP-09); the deployment only provides the relay the library already has.

#### 12.4 Events consumed

None. No consumer group is created by this release; the ledger writer is called over REST and consumes no topic (Architecture v5 slide 15).

#### 12.5 Workflows and activities

None. The writer is a synchronous REST service and this release registers no workflow, activity or worker on the task queue `rwb-source-data` of namespace `rwb-recovery`.

#### 12.6 Schedules

None. The deployment registers no Temporal Schedule and no Quartz job.

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| `interaction` | P1 (rwb_source_data) | The ledger table: migrated by this release, verified after the migration, and exercised by the smoke run |
| `processed_event` | PLT library, created in rwb_source_data | The inbox; created and used by the library, not by this release |
| `idempotency_key` | PLT library, created in rwb_source_data | The stored response of the append; the smoke run relies on it for the replay |
| `outbox_event` | PLT library, created in rwb_source_data | The outbox of the decision-record library |

No other schema is migrated, created, altered or read by this release (DP-01, DP-15, DP-18).

#### 12.8 Contract fakes

None is deployed. The case fake and the decision-log fake of the contract run in the service environment and the smoke run appends against them; the real cross-service proof belongs to RWB-ITG-E1066-ITG.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The three ledger operations are the app story's; the probes are cluster-internal |
| Kafka | 0 published, 0 consumed | No topic of this service and no consumer group in this release |
| Temporal | 0 workflows, 0 activities, 0 Schedules | No worker on `rwb-source-data` |
| File | None | No file is read or written by the deployment |
| SQL | One schema migrated, one table verified | `rwb_source_data`; the ledger objects of section 11 |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release migrates `rwb_source_data` only and reads no other schema | none |
| DP-03 | DecisionLogWriter, decision log | The local decision-record library is deployed with the service and publishes to `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE read in this release; the smoke entry names no ACE object | none |
| DP-07 | Reference data, LOV | The rwb-case reference-data contract is a run-time dependency of the append; the deployment configures nothing of it | H RWB-PLT-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | The library objects in `rwb_source_data` and the outbox relay of the service | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | The append is reached over REST through gateway-bff; the smoke run uses the same path | none |
| DP-13 | `/api/recovery/v1` | The ingress serves `/api/recovery/source-data/v1` and no other base | none |
| DP-15 | V0001 baseline, migration | The per-service Flyway sequence of `rwb_source_data`; the migration step refuses another schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | The ledger table is P1's and is deployed here; no other service's ledger object exists | none |
| DP-19 | Screen, ace-web | gateway-bff serves the recording screens; the deployment registers the route and no screen of its own | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-source-data/` overlay | API deployment, config map, secret references, probes, ingress route for the ledger operations, namespace and build ID |
| `helm/rwb-source-data/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, build ID, alert thresholds and windows (GAP-0506; ASM-0698) |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration step, verification step, trigger step, smoke run, promotion |
| Migration step | The `rwb_source_data` migration of this release, ledger version included; a target schema other than `rwb_source_data` is refused |
| Verification step | The catalogue check of the eight columns, the two unique keys, the trigger and the index, and the repeated-run check |
| Trigger step | One `UPDATE` and one `DELETE` on a synthetic row inside a rolled-back transaction; either statement succeeding fails the release |
| Dashboards | The five series of section 11 with the three dimensions |
| Alerts | Three rules, each with its message identifier or incident code and one runbook entry |
| Runbook | Three entries: append failure, ledger incident, missing trigger |

**Alert mapping**

| Identifier | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-022 | The append failure rate is past its threshold, or one append fails with 503 | Append failure alert naming the error class, the release and the build ID, with the rate and the window | Platform on-call, page (route and window are environment values: GAP-0506; ASM-0698) |
| LEDGER_WRITE_FAILED | The writer raised the incident `LEDGER_WRITE_FAILED` for a case | Ledger incident alert naming the case ID, the error class and the build ID, with no summary and no contact point | Platform on-call and the recovery on-call, ticket (route is an environment value: GAP-0506; ASM-0698) |
| Not specified in the source documents (GAP-0506; ASM-0698) | `tr_interaction_append_only` is missing or disabled after a migration | Trigger alert naming the table and the object, and failing the release when it is raised in a pipeline | DevOps on-call, page |

**Rollback.** A release that fails the smoke run is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own image digest and build ID; the ledger rows written by the new build stay, because an entry is never deleted and never updated, and the previous build serves the append against the same table. The migration is forward only: a wrong ledger version is corrected by a new version and never by editing an applied one (DP-15). The series show both build IDs while the two builds overlap, so a duplicate hit or a `case_seq` gap is attributable to one of them.

**Feature switch.** `rwb.dataengine.ledger-writer`. On: the writer is deployed and the append answers through gateway-bff. Off: the writer is not deployed in that environment, the append is refused at the edge, no entry is written and no append series is emitted; the rest of the service is unchanged.

**Done when.** The chart renders for DEV, SIT and UAT with a pinned digest and the build ID, the migration step refuses a foreign schema, the verification step finds the eight columns, the two keys, the trigger and the index in each environment, a repeated migration changes nothing, the five series and the three alerts are published with their identifiers or placeholders and their runbook links, the smoke run appends one synthetic entry and replays its key with one row in the table, and the three runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | An append fails, or its failure rate is past its threshold | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| LEDGER_WRITE_FAILED | The writer raised the ledger incident for a case | Not specified in the source documents (GAP-0506; ASM-0698) |
| Identifier pending | `tr_interaction_append_only` is missing or disabled | Not specified in the source documents (GAP-0506; ASM-0698) |

MSG-P1-022 keeps its legacy text unchanged and is the message of the append failure alert. The ledger incident and the trigger alert have no agreed text in the source set, and the threshold, the window and the route of each alert are not given either, so both are carried as the placeholder until the Error and Message Standard names them (GAP-0506; ASM-0698). An alert payload names counts, error classes, case IDs and build IDs only, never a summary, a contact point or an amount.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard, the alert route and the runbook. The recording screens and the case timeline that reach the append are served by rwb-case and by the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), and this deployment only registers the route. The platform administrator reads the release result and the ledger series under Platform administration R, and internal audit reads the append history and the release record under the same right.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1066-OPS-01 | AC1 | NFR | The chart renders for three environments with a pinned digest, the build ID, the `rwb_source_data` login reference and the route; a foreign migration target is refused |
| TC-P1-E1066-OPS-02 | AC2 | NFR | The flag on and off in two environments; the values file is the only source of the value |
| TC-P1-E1066-OPS-03 | AC3 | NFR | The catalogue after the migration: eight columns, a nullable channel and direction, two unique keys, the trigger and the index; a repeated run changes nothing |
| TC-P1-E1066-OPS-04 | AC4 | NFR | A synthetic run, failed appends and a duplicate key; the five series carry the three dimensions |
| TC-P1-E1066-OPS-05 | AC5 | NFR | Three simulated conditions raise the three mapped alerts, each with one runbook entry and no hard-coded threshold |
| TC-P1-E1066-OPS-06 | AC6 | NFR | One synthetic entry appended in DEV, the same key replayed with one row, and a rollback to the previous build with the same build ID recorded |
| TC-P1-E1066-OPS-07 | AC3 | NFR | The tables of section 12.7: only `interaction` is migrated and verified by this release; `processed_event`, `idempotency_key` and `outbox_event` are created by the library in rwb_source_data and not altered here; a read or write against another schema is refused |
| TC-P1-E1066-OPS-08 | AC9 | NFR | A build that fails its tests or its smoke run is not deployed; the previous build keeps serving and no ledger object changes |
| TC-P1-E1066-OPS-09 | AC10 | NFR | Not specified in the source documents (NEWAC-RWB-P1-E1066-OPS-AC10) |
| TC-E1-066-01 | AC1, BR2, BR3 — regression evidence: AC1 is owned by the rwb-case and rwb-integration slices of this key | End to end | Case RW-2026-000201 with 6 entries; outbound call with promise 25,000.00 |
| TC-E1-066-02 | AC2, BR1, BR7 — regression evidence: AC2 is owned by the recovery slices and the cross-service proof | End to end | 4 EFS entries, CASE_CREATED and CASE_ALLOCATED |
| TC-E1-066-03 | AC3, BR6 — regression evidence: AC3 is owned by the rwb-case slice and the rwb-decision contract | End to end | Reassignment under R-UNI-18 version 2026.11 |
| TC-E1-066-04 | AC4, BR5 — regression evidence: AC4 is owned by the rwb-integration slice and the cross-service proof | End to end | Insert forced to fail |
| TC-E1-066-05 | AC5 — regression evidence: AC5 is owned by RWB-P1-E1066-APP | End to end | append() with no event code |
| TC-E1-066-06 | AC6, BR7 — regression evidence: AC6 is owned by RWB-P1-E1066-APP | End to end | Two concurrent appends on one case |
| TC-E1-066-07 | AC7 — run by RWB-P1-E1066-APP | End to end | Unknown case ID |
| TC-E1-066-08 | AC8, BR4 — run by the cross-service test: AC8 is owned by the migration trigger of this key and verified here | End to end | UPDATE and DELETE on entry case_seq 3; CORRECTION entry |
| TC-E1-066-09 | Access — regression evidence: the access path belongs to the rwb-case slice | Component | RW-AUDIT posts an interaction; refused with MSG-P4-002 |

The nine operations test cases are this story's and run against the artefacts of a deployment. The nine legacy test case IDs are kept in order and their Covers and Data are carried onto the split, with the legacy level "System" mapped to "End to end" and "Access" to "Component"; they are regression rows here because the criteria they cover are owned by the slices named in each Covers cell. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; TC-P1-E1066-OPS-07, TC-P1-E1066-OPS-08 and TC-P1-E1066-OPS-09 are new and not yet in that workbook.

### 17. Guardrails

- No business value in a values file: the event codes, the channels, the directions and the case states are reference data and application behaviour, never a deployment value.
- No personal data in logs, series, alert payloads, the runbook or the smoke data: counts, error classes, case IDs and build IDs only; the smoke summary is synthetic, and no production payload is copied into a fixture.
- One login, one schema and one sequence: the release carries the `rwb_source_data` login and migrates `rwb_source_data` only (DP-02, DP-15).
- The release migrates, verifies and exercises the ledger table and no other service's schema; the ledger is P1's (DP-01, DP-18).
- The append-only trigger is verified on every environment and never assumed; a missing trigger blocks the release (BR2).
- No secret is written into a values file, a chart template, a dashboard or the runbook; the credential comes from the platform secret store.
- An applied migration is never edited: a wrong ledger version is corrected by a new version (DP-15).
- A failing smoke run never replaces a working build, and a rollback keeps the previous digest and build ID (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-ILG-001 | One ledger holds every interaction on a case | The `rwb_source_data` migration, the ledger table and the shared deployment of one service | TC-P1-E1066-OPS-01, TC-P1-E1066-OPS-03 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | The eight columns verified after the migration | TC-P1-E1066-OPS-03 |
| REQ-ILG-004 | Offer, promise, payment or hand-over recorded on its interaction | The append rate and the smoke entry that carries a promise in a synthetic case | TC-P1-E1066-OPS-04, TC-P1-E1066-OPS-06 |
| REQ-ILG-008 | A failed ledger write loses no entry and is reported | The append failure series, the MSG-P1-022 alert and the ledger incident alert | TC-P1-E1066-OPS-04, TC-P1-E1066-OPS-05 |
| REQ-ILG-007 | One entry per key; a repeat is ignored and counted | The idempotency table, the duplicate hits series and the replay step of the smoke run | TC-P1-E1066-OPS-04, TC-P1-E1066-OPS-06 |
| ADR-023 | Observability per service | The five series, the three alerts and the three runbook entries | TC-P1-E1066-OPS-04, TC-P1-E1066-OPS-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1066-APP | App development | Sibling: the writer and the ledger migration this release deploys and verifies |
| RWB-P1-E1066-CON | Contract | Sibling: the three ledger operations and the fakes the smoke run uses |
| RWB-P1-E1067-APP | App development | Sibling of the same legacy key: the outbox path whose appends the failure series also shows |
| RWB-ITG-E1066-ITG | Integration | Proves the append, the duplicate rule and the trigger against the live rwb-case and rwb-decision contracts |
| RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the libraries and the sequence the release is built on |
| RWB-PLT-NF06-DB, RWB-P1-E1001-APP | ACE DB and App development | Prerequisites: the schema, the login and the baseline the ledger migration sits on |

### 19. Out of scope

- The writer, the controller, the repository and the migration as code (RWB-P1-E1066-APP).
- The contract documents, the schemas, the error envelope and the fakes (RWB-P1-E1066-CON); this story only deploys, verifies and gates them.
- The outbox path from a business event to an entry (RWB-P1-E1067-APP).
- The ledger read interface and its filters (RWB-P1-E1068-APP).
- The recording screens and the case timeline of rwb-case (RWB-P3-E1018-APP and the screen owners).
- The real cross-service proof of the append, the duplicate rule and the append-only behaviour against the live rwb-case and rwb-decision contracts (RWB-ITG-E1066-ITG).
- The platform components: the Kafka topics and the schema registry, the Temporal cluster and its namespace, the flag library, the secret store and the observability platform (the platform epics).
- The exact deployment topology, resource sizes, replica counts, probe timings, alert thresholds, windows and the incident route; they are set per environment by the platform team (GAP-0506; ASM-0698).
- The Error and Message Standard texts of the ledger incident and of the trigger alert (the standard owner); both are carried as placeholders.
