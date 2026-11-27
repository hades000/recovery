# RWB-P1-E1066-OPS Interaction ledger store and writer

SCB Collections and Recovery. Henka Group, 27 November 2026.
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
| Size | Not specified; pending squad refinement |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P1-Q |
| Ready to start | After the base release of RWB-P1-E1015-OPS and the E1066-APP migration; the intake deployment step follows the E1067-APP listener as a later step (RD-P1-074) |
| Depends on (build) | RWB-P1-E1001-APP, RWB-P1-E1015-OPS, RWB-PLT-NF06-DB, RWB-P1-E1066-APP, RWB-P1-E1066-CON, RWB-P1-E1067-CON, RWB-PLT-E1047-CON |
| Contract dependencies | None |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), base `/api/recovery/source-data/v1` |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1067-APP listener, for the intake deployment step only; no build dependency (RD-P1-074) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v2.md (FR-P1-029, FR-P1-030) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-007, RD-P1-009 (X-03), RD-P1-028, RD-P1-044, RD-P1-045, RD-P1-074 |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- Delta release on the base of RWB-P1-E1015-OPS (RD-P1-044): ledger migration, flag, ledger series and alerts, smoke run and the three ledger-intake consumer groups (RD-P1-003, RD-P1-009, X-03).
- Case-scoped smoke path, replay status, flag-off answer, rollback standard and PROD verification fixed (RD-P1-001, RD-P1-007, RD-P1-045).
- Acceptance criteria rewritten; AC10 withdrawn; AC18 and AC19 added; test case IDs of Test Cases v9 cited.
- Findings RWB-P1-E1066-OPS#1 to #24 fixed or carried as pending with a gap ID (GAP-0506, GAP-3506, S8-8, S8-9, S8-10).
- Batch D: the build cycle with RWB-P1-E1067-APP is cut (RD-P1-074): this story no longer depends on the intake application to build; the intake deployment step follows it. Test case IDs TC-P1-E1066-OPS-22 and -23 cited.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register); applied RD-P1-001, RD-P1-003, RD-P1-007, RD-P1-009 (X-03), RD-P1-028, RD-P1-044 and RD-P1-045; findings RWB-P1-E1066-OPS#1 to #24.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-066 for rwb-source-data. The single deployment of the monolith becomes the release of the ledger writer on its own chart, with the `rwb_source_data` sequence applied by its own migration step (DP-15), the ledger table, its two unique keys and its append-only trigger verified after the migration, the flag `rwb.dataengine.ledger-writer` gating the writer, five series and three alerts with one runbook entry each (ADR-023), and a smoke run that appends one synthetic entry and replays the same key. The ledger itself stays P1's table in `rwb_source_data` (DP-01, DP-18; the R-PREC default ruling) and no other service's schema is migrated or read. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1066-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (7 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the ledger writer of rwb-source-data released as a delta of the service chart on DEV, SIT, UAT and PROD with a pinned image digest and build ID, the `rwb_source_data` migration applied by its own step, the ledger table verified with its columns, its two unique keys, its append-only trigger and its index, the flag `rwb.dataengine.ledger-writer` to turn the writer on and off, five dashboard series, three alerts each with one runbook entry, the three ledger-intake consumer groups, and a smoke run that appends one synthetic entry and replays the same key without writing a second row**, so that **an operator can see the append rate and its failures, prove that a repeated key writes nothing, and roll back to the previous build without losing or duplicating an entry**.

### 2. Business rationale

The legacy story assumed one process in one module: the ledger table, the writer and the incident hook were in the same deployment, so a failed append was a row in the log of the same application that took the call. In the target the writer is a service of its own, its table lives in its own schema, and the callers are a screen through gateway-bff and an event path of rwb-integration (DP-01, DP-11, DP-19; Architecture v5 slides 11, 29 and 41).

That separation is what this story makes operable. A table that is created by the wrong schema, an append-only trigger that is missing after a migration, a `case_seq` sequence with a gap because a second pod allocated the same number, or an append that fails silently in one environment are all conditions that no unit test of the writer can see, and each of them breaks the one promise of the ledger: the history has no gap. The release therefore verifies four things on every environment instead of trusting the migration once: that the ledger columns and both unique keys exist, that the append-only trigger is present and refuses an update, that a repeated `Idempotency-Key` returns the same entry and the same `caseSeq`, and that an append failure is visible on a series and raises its alert with MSG-P1-022.

Observability follows ADR-023 per service and keeps the personal-data rule of the platform: five series and three alerts carry counts, classes, codes and build IDs only, never a summary and never a contact point (Architecture v5 slide 11). The deployment also enforces the ownership boundary operationally: the release carries the `rwb_source_data` login only, applies the `rwb_source_data` migration only, and refuses any other target schema (DP-01, DP-02, DP-15).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The `rwb_source_data` schema, its login and the per-service Flyway sequence exist, delivered by RWB-PLT-NF06-DB and the baseline of RWB-P1-E1001-APP (DP-02, DP-15).
- The base release of RWB-P1-E1015-OPS exists: the chart skeleton, values files, api and worker Deployments, probes, migration job, login secret reference and standard service alerts. This story adds values keys and its own objects only (RD-P1-044 rules a and b); the base is `/api/recovery/source-data/v1` behind gateway-bff.
- The ledger migration of RWB-P1-E1066-APP is merged on the service sequence, and its version is the one this release applies; the writer and the migration ship together.
- The contract of RWB-P1-E1066-CON is published, so the smoke run can call POST /cases/{caseId}/interactions and GET /cases/{caseId}/interactions/{entryId} with a known shape.
- The case fake and the decision-log fake of the contract are available in DEV, so the smoke run appends a synthetic entry without a live rwb-case or rwb-decision. The case target of the smoke run in SIT and UAT, its identity and grant, and the reserved synthetic case ID are pending (GAP-3495).
- The flag library is in force and the flags `rwb.dataengine.ledger-writer` and `rwb.dataengine.ledger-events` are registered for DEV, SIT, UAT and PROD.
- The platform secret store holds the `rwb_source_data` credential, and no secret appears in a values file, a chart template, a dashboard or the runbook.
- The observability platform of ADR-023 is in force, so a series can carry the environment, the release and the build ID as dimensions.
- Alert thresholds and channel names are per-environment values-file entries of rwb-source-data (Observability and Monitoring Design v6; RD-P1-028); the ledger-specific threshold values, probe timings and runbook routes are given by no source (GAP-0506; ASM-0698). The standard service alerts use error rate 5xx above 1 percent for 5 minutes and latency p95 above 2 seconds for 15 minutes (Observability and Monitoring Design, section 2.1).
- The build dependencies of the header are merged; this story is not a Day 1 story.

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version with one image digest.
2. The release uses the chart of the base release (RWB-P1-E1015-OPS) and adds only the ledger values keys, the intake consumer groups and the ledger alerts; a rendered chart diff shows no change to an object this story does not own (RD-P1-044).
3. The migration job applies the next version of the `rwb_source_data` sequence, `V<next>__rwb_e1_066_interaction_ledger.sql` of RWB-P1-E1066-APP, which adds `uk_interaction_case_seq`; it refuses a target schema other than `rwb_source_data`. The migration is expand-only (RD-P1-045).
4. The verification step reads the catalogue and the Flyway history: the named version is successful, the baseline ledger columns and nullable `channel` and `direction`, `uk_interaction` (idempotency key), `uk_interaction_case_seq` (case_id, case_seq), the trigger `tr_interaction_append_only` and the index `ix_interaction_case_time` exist.
5. In DEV, SIT and UAT the trigger step attempts one `UPDATE` and one `DELETE` on a synthetic row inside a transaction it rolls back, and fails the release when either statement succeeds. PROD runs catalogue reads only.
6. The flag step sets `rwb.dataengine.ledger-writer` and `rwb.dataengine.ledger-events` from the values of the environment. With the writer flag off the api answers 404 on the append path; with the intake flag off the three consumer groups are paused (EDD v6 Table 8; RD-P1-009 rule 8; RD-P1-045).
7. The dashboards are published with the five series of section 11 and the environment, release and build ID as dimensions; no case ID is a metric label.
8. The three ledger alerts are wired to their runbook entries and routed to the owning service rwb-source-data with the platform administrator as first recipient.
9. The smoke run (DEV) appends one entry for the reserved synthetic case through `POST /cases/{caseId}/interactions`, reads it with `GET /cases/{caseId}/interactions/{entryId}`, re-sends the same `Idempotency-Key` and body and confirms the replayed 201 with the same entry ID and `caseSeq`. The synthetic row is permanent because the ledger is append only; no smoke append runs in PROD.
10. The release is promoted only when the checks of steps 3 to 9 pass; a failing check leaves the previous build in force.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The deployment stays unready and the pipeline stops; no traffic is served | None | AC1 |
| X2 | The migration step is pointed at a schema other than `rwb_source_data` | The step refuses and records the refused target; no object is created | Pipeline error, no message id | AC1 |
| X3 | The migration ran but a ledger column, a unique key, the trigger or the index is missing | The verification step fails the release and names the missing object | Pipeline error, no message id | AC3 |
| X4 | The append-only trigger is missing or disabled, or an `UPDATE` or `DELETE` succeeds on a ledger row | The release fails; the trigger alert fires and names the object. Detection between releases is pending (GAP-3494) | The alert carries no message ID (GAP-0506) | AC3, AC5 |
| X5 | Appends fail | The failure series rises by class; the failure-rate alert fires when the rate passes its threshold; one single 503 does not page by itself | MSG-P1-022 | AC4, AC5 |
| X6 | `rwb.dataengine.ledger-writer` is off in an environment | The service stays deployed; the append path answers 404 and no entry is written | Pending (GAP-3506) | AC2 |
| X7 | The smoke run replays the same key and a second row appears | The smoke run fails the release and names the case, the key and the two `caseSeq` values | Pipeline error, no message id | AC6 |
| X8 | A new build is promoted while entries are being appended | The previous build drains and the new build takes new requests; both build IDs appear on the series | None | AC1, AC4 |

X1 and X2 are the deployment paths; X3 and X4 are the four facts the release verifies instead of assuming; X5 and X8 are the observability paths of ADR-023; X6 is the flag; X7 is the one assertion that proves the idempotency of the append in a live environment.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Delta on the base release; uses the flag library and the observability platform. The application code that emits the ledger series belongs to the APP stories |
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
    Given the base release of RWB-P1-E1015-OPS is deployed

  Scenario: AC1 The writer is released from one chart with one digest and one build ID (new, D-RCV-60)
    Given values files for DEV, SIT, UAT and PROD
    When the chart is rendered and the migration job runs
    Then each render pins the chart version and the image digest and carries the build ID of the release
    Then the release declares the rwb_source_data login and no other service's credential
    Then flyway history of rwb_source_data shows the ledger version of RWB-P1-E1066-APP as successful
    When the migration job targets another schema
    Then the job fails and no object is created

  Scenario: AC2 The flag turns the append on and off (new, D-RCV-60)
    Given rwb.dataengine.ledger-writer is on in SIT
    When a valid append is posted
    Then it answers 201
    Given the flag is off in SIT
    When a valid append is posted
    Then it answers 404, and no interaction, idempotency_key or outbox_event row is added
    Then the flag value comes from the values file of the environment and is never hard-coded in a template
    # Pending: messageCode of the 404 and the effect on the in-process writer; owner solution architect; GAP-3506.

  Scenario: AC3 The ledger objects exist after the migration and a repeated run changes nothing (new, D-RCV-60)
    Given the ledger version has been applied in SIT
    When the catalogue is read for the interaction table
    Then column types and lengths match Physical Schema v9 and channel and direction are nullable
    Then uk_interaction on (idempotency_key) and uk_interaction_case_seq on (case_id, case_seq) exist
    Then the trigger tr_interaction_append_only exists and is enabled for UPDATE and DELETE
    Then the index ix_interaction_case_time on (case_id, occurred_at) exists
    When the migration job runs again
    Then Flyway reports the version as already applied and no object changes

  Scenario: AC4 The five series carry the environment, the release and the build ID (new, D-RCV-60)
    Given the published dashboard of the deployment
    When 5 appends, 2 forced failures and 1 header replay run on the synthetic case
    Then the append rate rises by 5, the failures by 2 under their error class and the duplicate hits by 1
    Then the p95 append latency and the case_seq gap series are present
    Then each series carries environment, release and build ID and no case ID, summary or contact point label
    # Pending: metric names, types, the emitting component and the case_seq gap detection; owner solution architect; GAP-3494.

  Scenario: AC5 The three ledger alerts each link one runbook entry (new, D-RCV-60)
    Given the published alert rules and the runbook
    When the failure rate passes its threshold, an incident LEDGER_WRITE_FAILED is raised and the trigger is dropped in the pipeline environment
    Then the failure-rate alert fires with MSG-P1-022 and the build ID
    Then the incident alert names the incident code, the case ID and the error class and no summary
    Then the trigger alert names tr_interaction_append_only, and the trigger is restored and re-verified
    Then every alert reaches the platform administrator and links one runbook entry with check, owner role and recovery step
    Then thresholds and channel names come from the values files of the environment

  Scenario: AC6 The smoke run appends, replays and survives a rollback (new, D-RCV-60)
    Given the deployed writer in DEV, the case fake and N rows for the reserved synthetic case
    When the smoke run appends one entry with a new UUID Idempotency-Key and re-sends the same key and body
    Then the first answer is 201 and the replay returns the stored 201 with the same entry ID and caseSeq
    Then the case has N+1 rows
    When the writer flag is switched off and, if needed, the previous tag is redeployed
    Then the case still has N+1 rows and the previous build runs against the migrated schema
    Then no applied migration is reversed

  Scenario: AC7 The intake consumer groups are deployed by this release (new, RD-P1-003 and RD-P1-009; X-03)
    Given RWB-P1-E1067-CON and RWB-P1-E1067-APP are ready for deployment
    When this release is deployed
    Then one consumer group is deployed on each of `rwb.case.events.v1`, `rwb.document.events.v1` and `rwb.decision-record.v1`
    Then group IDs use the working pattern `rwb-source-data.<topic>` and first start uses `auto.offset.reset=earliest`
    Then no group is deployed for `rwb.source-data.events.v1`
    Then the groups pause when rwb.dataengine.ledger-events is off and resume from the committed offset when it is on
    Then the rwb-source-data principal can read the three topics and their retry topics and write their retry and dead-letter topics, as granted by RWB-PLT-N002-INF
    Then this OPS story declares the groups and E1067-APP owns the listener runtime

  # AC8 does not exist in this story.

  Scenario: AC9 A failing release never replaces a working build (new, D-RCV-60)
    Given build B1 serves
    When build B2 fails its tests or its smoke run after its migration applied
    Then B2 is not promoted, B1 serves with its own digest and a B1 append returns 201 on the migrated table

  # AC10 withdrawn: not applicable, a deployment story has no ledger status model.

  Scenario: AC11 TRUNCATE and trigger change are refused (new, D-RCV-60)
    Given the runtime login of rwb-source-data
    When TRUNCATE interaction or ALTER TABLE interaction DISABLE TRIGGER is attempted
    Then each statement is refused and the row count is unchanged
    # Pending: the mechanism (separate migration owner role or TRUNCATE guard); owner data architect; GAP-3493.

  Scenario: AC12 Another service login cannot reach the ledger (new, D-RCV-60)
    Given the login of another service
    When it selects from or inserts into rwb_source_data.interaction
    Then the database refuses with a permission error

  Scenario: AC13 A failed migration leaves the previous build serving (new, D-RCV-60)
    Given a previous build and a migration that fails part way
    When the pipeline runs
    Then no object of that version remains, the pipeline fails and the previous build serves

  Scenario: AC14 Readiness and liveness are separate (new, D-RCV-60)
    Given a new pod and an unreachable database
    When health probes run
    Then readiness fails, liveness passes and no ledger row is written

  Scenario: AC15 No personal data or secret reaches logs and alerts (new, D-RCV-60)
    Given a forced failed append with a marker string in summary
    When logs, series labels and alert payloads are searched
    Then neither the marker nor a credential appears

  Scenario: AC16 Standard service alerts cover the ledger operations (new, D-RCV-60)
    Given the standard service alerts owned by RWB-P1-E1015-OPS
    When 5xx on the ledger operations is above 1 percent for 5 minutes or p95 is above 2 seconds for 15 minutes
    Then the alert names rwb-source-data and reaches the platform administrator
    Then this release declares no second copy of those alerts

  Scenario: AC17 PROD verification writes no ledger row (new, D-RCV-60)
    Given a PROD release
    When verification runs
    Then only catalogue reads run and the pipeline adds no interaction row

  Scenario: AC18 The release changes only what it owns (new, RD-P1-044)
    Given the rendered chart of the base release and of this release
    When they are compared
    Then only the ledger values keys, the three intake consumer groups and the ledger alerts differ

  Scenario: AC19 The previous tag passes its smoke test on the new schema (new, RD-P1-045)
    Given the ledger migration is applied
    When the pipeline runs the previous tag's smoke test against the migrated schema
    Then it passes; if it fails the release is not promoted
```

**Target reading.** The criteria are new, because the legacy story had no deployment section. This story is a delta of the service release (RD-P1-044): the base chart, Deployments, probes, migration job and standard alerts belong to RWB-P1-E1015-OPS. The table is P1's and no other service's schema is migrated or read (DP-01, DP-18). Rollback follows RD-P1-045: flag off first, previous image only if the flag does not cover the fault, no migration reversed; a release is rolled back when the post-deploy checks fail, the platform smoke workflow JOB-22 reports no result for the day, or an incident is attributed to it. On a first release rollback is flag off, the api answers 404 on the append path and the intake groups stay paused.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login, one schema and one sequence per service: the release carries the `rwb_source_data` login and migrates `rwb_source_data` only | Architecture v5 slides 11 and 29; DP-02, DP-15 |
| BR2 | The ledger table, its two unique keys and its append-only trigger are verified after every migration on every environment (catalogue reads in PROD), and a missing object fails the release | REQ-ILG-001; R-UNI-24; legacy RWB-E1-066 BR4 |
| BR3 | A repeated `Idempotency-Key` writes no second row and returns the same entry and the same `caseSeq` | REQ-ILG-007; DP-09; Architecture v5 slide 11 |
| BR4 | Every alert carries a message ID or a named incident code and links one runbook entry | Template and Rules §R7.2 s14; ADR-023 |
| BR5 | No environment value is hard-coded: replicas, resources, probe timings, thresholds, windows, channel names and flags come from the values files of the environment | RD-P1-028; Observability and Monitoring Design v6; GAP-0506 |
| BR6 | Series labels carry counts, classes, codes, environment, release and build ID only; a case ID appears only in the incident alert; never a summary, contact point or amount | Architecture v5 slide 11 (PDPA); ADR-023 |
| BR7 | The release writes no ledger entry except the permanent synthetic smoke entry outside PROD, and reads no other service's table | DP-01; DP-18; RD-P1-007 |
| BR8 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run | DP-15; RD-P1-045; AC9, AC19 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Migration applied and the ledger objects verified | The eight columns, the two keys, the trigger and the index are present | Ready |
| Deploying | Verification failed | A column, a key, the trigger or the index is missing | Blocked |
| Ready | Release superseded | A new chart version passes its tests and its smoke run | Rolling |
| Rolling | All pods on the new build | The previous build drains | Ready |
| Ready | Writer flag off | `rwb.dataengine.ledger-writer` is turned off in the environment | Ready, append path answering 404 |
| Ready | Smoke run failed | The append, the replay or the rollback step fails | Blocked |
| Blocked | Previous build restored | The flag is off and, if needed, the previous tag is redeployed | Ready |

The ledger entry has no status and is never changed; the states above are states of the deployment and not of a row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the secret store, the flag library and the ingress route |
| ACE database administrator | Confirms the migration ran on `rwb_source_data` and the grants of the schema; the protection of the append-only objects from the owning login is pending (GAP-3493) |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the three runbook entries, including a persisting `case_seq` gap under the append-failure entry, and opens an incident when needed |
| RW-AUDIT | Reads the append history and the release record |
| RW-PLATADM, platform administrator role | First recipient of the ledger alerts (Observability and Monitoring Design, section 2.2); reads the series and receives the incident |

The release runs as the `rwb_source_data` service identity (DP-02), carried by the chart as a secret reference and never as a literal credential.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, build ID, flag values, alert thresholds, windows and channel names (RD-P1-028; GAP-0506) | Not a business field |
| Schema | `rwb_source_data`, migrated by its own per-service Flyway sequence; this release applies the ledger version | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Ledger objects | The `interaction` table with `event_code`, `actor_type`, `actor_ref`, `source_ref`, `idempotency_key`, `case_seq`, `decision_log_id` and `corrects_entry_id`, a nullable `channel` and `direction`, the unique keys `(case_id, case_seq)` and `(idempotency_key)`, the trigger `tr_interaction_append_only` and the index `ix_interaction_case_time` | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Platform library objects | `processed_event`, `idempotency_key` and `outbox_event`, created in `rwb_source_data` by the library (DP-09) | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Series | Append rate, append failures by error class, duplicate hits, p95 latency of the append, `case_seq` gaps; dimensions environment, release, build ID; metric names pending (GAP-3494) | Not a business field |
| Alerts | Append failure rate with MSG-P1-022; incident `LEDGER_WRITE_FAILED` with case ID and error class; missing or disabled `tr_interaction_append_only` | Not a business field |
| Runbook entries | Append failure, ledger incident, missing trigger; each with the check, the owner role and the recovery step | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Secrets | The `rwb_source_data` credential, from the platform secret store; no other credential is carried | Not specified in the source documents (DOR-RWB-P1-E1066-OPS-7) |
| Test data | One permanent synthetic entry per smoke run for the reserved synthetic case in DEV, with no personal data and no promise value, excluded from PROD; the reserved case ID is pending (GAP-3495) | Not a business field |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded (GAP-0506; ASM-0698).

**Probes.** Readiness is healthy when the ledger migration version is present and the database is reachable; it does not wait for a served request. Liveness is healthy when the process is up and its loop is responsive. The probe paths are those of the base release. Neither probe writes a ledger row or commits a transaction.

### 12. Contract

#### 12.1 REST operations provided

None from this story. `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` and `GET /api/recovery/source-data/v1/cases/{caseId}/interactions/{entryId}` are declared by RWB-P1-E1066-CON and implemented by RWB-P1-E1066-APP, and the list read `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` is implemented by RWB-P1-E1068-APP; this deployment exposes them through the chart and the ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None from the deployment. The migration step, the verification step, the trigger step and the smoke run read the catalogue and call the service under test; the chart carries no REST client of its own, no composite route and no outbound call at start-up.

#### 12.3 Events published

None. The topic `rwb.source-data.events.v1` carries `AceDataReady` and `AceDataLate`, which belong to RWB-P1-E1015-APP and are published in RWB-P1-E1015-CON, and this release publishes neither. The ledger append produces no decision record; acting services record their own decision through the decision-record library.

#### 12.4 Events consumed

This release deploys the three ledger-intake consumer groups owned by RWB-P1-E1067-APP. Group IDs use the working pattern `rwb-source-data.<topic>` (ASM-5691), one group per topic. No group is created for `rwb.source-data.events.v1`.

| Topic | Consumer group | Runtime owner |
|---|---|---|
| `rwb.case.events.v1` | `rwb-source-data.rwb.case.events.v1` | RWB-P1-E1067-APP |
| `rwb.document.events.v1` | `rwb-source-data.rwb.document.events.v1` | RWB-P1-E1067-APP |
| `rwb.decision-record.v1` | `rwb-source-data.rwb.decision-record.v1` | RWB-P1-E1067-APP |

First start uses `auto.offset.reset=earliest`. When `rwb.dataengine.ledger-events` is off, the groups are paused and resume from the committed offset when it is on. Records older than the 7-day topic retention are recovered only from `.dlt` through the platform replay tool. RWB-PLT-N002-INF creates the topics, retry and dead-letter topics and ACLs; this story verifies the read ACL on the three topics and their retry topics and the write ACL on the retry and dead-letter topics.

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

None is deployed. The case fake and the decision-log fake of the contract run in DEV and the smoke run appends against them; the real cross-service proof belongs to RWB-ITG-E1066-ITG.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The three ledger operations are the app story's; the probes are cluster-internal |
| Kafka | 0 published, 3 consumed | This release deploys the three ledger-intake consumer groups; no group on `rwb.source-data.events.v1` |
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
| `helm/rwb-source-data/` values keys | Ledger flags, consumer groups, ledger alert rules; no redefinition of base objects (RD-P1-044) |
| `helm/rwb-source-data/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml`, `values-prod.yaml` | Flag values, alert thresholds, windows and channel names of this story (GAP-0506); PROD promotion follows the monthly change window with the release owner and the application owner (EDD v6) |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration step, verification step, trigger step, smoke run, promotion |
| Migration step | Base migration job applying `V<next>__rwb_e1_066_interaction_ledger.sql`; another target schema is refused |
| Verification step | Catalogue and Flyway history check of the named version, columns, `uk_interaction`, `uk_interaction_case_seq`, trigger and index, and the repeated-run check |
| Trigger step | One `UPDATE` and one `DELETE` on a synthetic row inside a rolled-back transaction; either statement succeeding fails the release |
| Dashboards | The five series of section 11 with the three dimensions |
| Alerts | Three rules, each with its message identifier or incident code and one runbook entry |
| Runbook | Three entries: append failure (including a `case_seq` gap), ledger incident, missing trigger |

**Alert mapping**

| Identifier | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-022 | The append failure rate is past its threshold | Append failure alert naming the error class, release and build ID, with rate and window | rwb-source-data; platform administrator first; channel from values (GAP-0506) |
| LEDGER_WRITE_FAILED | Raised by the intake after exhausted retries (RWB-P1-E1067-APP) or by a calling service for its refused action; the REST writer raises none. The signal that survives a database outage is pending (GAP-3494) | Ledger incident alert naming case ID, error class and build ID, no summary or contact point | rwb-source-data; platform administrator first |
| No message ID (GAP-0506) | `tr_interaction_append_only` is missing or disabled; checked at each release, periodic check pending (GAP-3494) | Trigger alert naming table and object; fails the release in a pipeline | rwb-source-data; platform administrator first |

**Rollback (RD-P1-045).** Switch `rwb.dataengine.ledger-writer` and, for intake faults, `rwb.dataengine.ledger-events` off first. Only if the flag does not cover the fault, redeploy the previous image tag and chart version; the release note names every P1 capability the redeploy reverts. No migration is reversed and no ledger row is deleted; a wrong ledger version is corrected by a new forward version. Kafka consumer offsets are not reset. On a first release, rollback is flag off: the api answers 404 on the append path.

**Feature switch.** `rwb.dataengine.ledger-writer`: on, the append answers through gateway-bff; off, the service stays deployed, the append path answers 404, no entry is written and no append series is emitted; the two reads are not flagged by this switch. `rwb.dataengine.ledger-events` pauses the intake groups. Defaults per environment are set by the release owner in the values files (GAP-3506 for the messageCode).

**Done when.** The chart renders for the four environments with a pinned digest and build ID, the migration job refuses a foreign schema, the verification step finds the named version and objects, a repeated migration changes nothing, the series and alerts are published with runbook links, the DEV smoke run passes and replays with one row, the previous tag passes its smoke test on the migrated schema, and the runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | An append fails, or its failure rate is past its threshold | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| LEDGER_WRITE_FAILED | The intake or a calling service raised the ledger incident for a case | Incident code; MSG-P1-022 in the detail |
| Identifier pending | `tr_interaction_append_only` is missing or disabled | Not specified in the source documents (GAP-0506; ASM-0698) |

MSG-P1-022 keeps its legacy text unchanged and is the message of the append failure alert. The trigger alert has no agreed message in the source set (GAP-0506; ASM-0698). A single 503 raises no page; the rate alert and the incident are separate signals. An alert payload names counts, error classes, case IDs (incident only) and build IDs, never a summary, contact point or amount.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard, the alert route and the runbook. The recording screens and the case timeline that reach the append are served by rwb-case and by the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), and this deployment only registers the route. The platform administrator reads the release result and the ledger series under Platform administration R, and internal audit reads the append history and the release record under the same right.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1066-OPS-01 | AC1 | NFR | Four renders, pinned digest, foreign migration target |
| TC-P1-E1066-OPS-10 | AC2 | NFR | Writer flag on and off |
| TC-P1-E1066-OPS-03, TC-P1-E1066-OPS-07 | AC3 | NFR | Catalogue and repeated migration |
| TC-P1-E1066-OPS-11 | AC4 | NFR | 5 appends, 2 failures, 1 replay |
| TC-P1-E1066-OPS-12 | AC5 | NFR | Three alert conditions |
| TC-P1-E1066-OPS-13 | AC6 | NFR | Append, replay, rollback on the synthetic case |
| TC-P1-E1066-OPS-14 | AC7 | NFR | Three intake consumer groups and flag pause |
| TC-P1-E1066-OPS-08 | AC9 | NFR | Failing build never replaces the serving build |
| TC-P1-E1066-OPS-15 to TC-P1-E1066-OPS-21 | AC11 to AC17 | NFR | Database refusals, failed migration, probes, log search, standard alerts, PROD verification |
| TC-P1-E1066-OPS-22, TC-P1-E1066-OPS-23 | AC18, AC19 | NFR | Chart diff; previous tag smoke on the new schema |

TC-P1-E1066-OPS-09 tests the withdrawn AC10 and is retired. The legacy cases TC-E1-066-01 to TC-E1-066-04, TC-P1-E1066-APP-15 to TC-P1-E1066-APP-17, TC-E1-066-08, TC-E1-066-09 belong to the APP, CON and integration slices and are not run by this story.

### 17. Guardrails

- No business value in a values file: the event codes, the channels, the directions and the case states are reference data and application behaviour, never a deployment value.
- No personal data in logs, series, alert payloads, the runbook or the smoke data: counts, error classes, case IDs and build IDs only; the smoke summary is synthetic, and no production payload is copied into a fixture.
- One login, one schema and one sequence: the release carries the `rwb_source_data` login and migrates `rwb_source_data` only (DP-02, DP-15).
- The release migrates, verifies and exercises the ledger table and no other service's schema; the ledger is P1's (DP-01, DP-18).
- The append-only trigger is verified on every environment and never assumed; a missing trigger blocks the release (BR2).
- No secret is written into a values file, a chart template, a dashboard or the runbook; the credential comes from the platform secret store.
- An applied migration is never edited: a wrong ledger version is corrected by a new version (DP-15).
- A failing smoke run never replaces a working build; a rollback redeploys the previous tag and keeps every ledger row (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-ILG-001 | One ledger holds every interaction on a case | The `rwb_source_data` migration and the verified ledger objects | TC-P1-E1066-OPS-01, TC-P1-E1066-OPS-03 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | The ledger columns verified after the migration | TC-P1-E1066-OPS-07 |
| REQ-ILG-008 | A failed ledger write loses no entry and is reported | The failure series, the rate alert and the incident alert | TC-P1-E1066-OPS-11, TC-P1-E1066-OPS-12 |
| REQ-ILG-007 | One entry per key; a repeat is ignored and counted | The duplicate hits series and the replay step of the smoke run | TC-P1-E1066-OPS-11, TC-P1-E1066-OPS-13 |
| ADR-023 | Observability per service | The five series, the three ledger alerts and the three runbook entries | TC-P1-E1066-OPS-11, TC-P1-E1066-OPS-12 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1066-APP | App development | Sibling: the writer and the ledger migration this release deploys and verifies |
| RWB-P1-E1066-CON | Contract | Sibling: the three ledger operations and the fakes the smoke run uses |
| RWB-P1-E1067-APP | App development | Sibling of the same legacy key: the outbox path whose appends the failure series also shows |
| RWB-ITG-E1066-ITG | Integration | Proves the append, the duplicate rule and the trigger against the live rwb-case and rwb-decision contracts |
| RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the libraries and the sequence the release is built on |
| RWB-PLT-NF06-DB, RWB-P1-E1001-APP, RWB-P1-E1015-OPS | ACE DB, App development, DevOps | Prerequisites: the schema, the login, the baseline and the base release |

### 19. Out of scope

- The writer, the controller, the repository and the migration as code (RWB-P1-E1066-APP).
- The contract documents, the schemas, the error envelope and the fakes (RWB-P1-E1066-CON); this story only deploys, verifies and gates them.
- The outbox path from a business event to an entry (RWB-P1-E1067-APP).
- The ledger read interface and its filters (RWB-P1-E1068-APP).
- The recording screens and the case timeline of rwb-case (RWB-P3-E1018-APP and the screen owners).
- The real cross-service proof of the append, the duplicate rule and the append-only behaviour against the live rwb-case and rwb-decision contracts (RWB-ITG-E1066-ITG).
- The platform components: the Kafka topics and the schema registry, the Temporal cluster and its namespace, the flag library, the secret store and the observability platform (the platform epics).
- The exact deployment topology, resource sizes, replica counts, probe timings, ledger alert threshold values and windows; they are set per environment in the values files (GAP-0506; ASM-0698).
- The base chart, Deployments, KEDA, migration job and standard service alerts (RWB-P1-E1015-OPS).
- The Error and Message Standard texts of the ledger incident and of the trigger alert (the standard owner); both are carried as placeholders.

### Remaining delivery steps

- Size the story at refinement; owner: squad.
- Obtain epic design sign-off; owner: product owner.
- Rule the flag-off messageCode; owner solution architect; GAP-3506.
- Rule the append-only protection against the owning login; owner data architect; GAP-3493.
- Rule metric names, emitting component, gap detection and the incident signal; owner solution architect; GAP-3494.
- Name the smoke identity and grant, the reserved synthetic case and the SIT and UAT case target; owner solution architect; GAP-3495.
- Set ledger alert thresholds, windows and runbook routes; owner solution architect; GAP-0506.
- Add or update story tests in Test Cases v9 (W2-tests); owner: test writer.
- Run the required test data in DEV after implementation; owner: delivery team.
