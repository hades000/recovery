---
run_id: INC-003-epic-1-RWB-E1-042
story: RWB-E1-042
title: Central configuration service and parameter catalog
stage: specify
revision: 3 (remediation of REVIEW-RWB-E1-042-SPEC-003; D-RUN-07, D-RUN-08, D-RUN-10)
prepared: 2026-11-17
author: Technical Specifier (agent run)
status: SUCCESS_WITH_ASSUMPTIONS
---

# Technical Specification: RWB-E1-042 Central configuration service and parameter catalog

| Field | Value |
|---|---|
| Story | RWB-E1-042, Central configuration service and parameter catalog (Enabler, Must) |
| Epic / design module | E1 / P3 Case and workflow (story v7 header); API `x-module` P3 for the read, P4 for loads |
| RUN_ID | `INC-003-epic-1-RWB-E1-042` |
| Build order | 3 of 72, Window 1 (Build Sequence v6). Depends on RWB-E1-044 (order 1) only |
| Source requirement | Traceability Matrix row `BR-RWB-010` / `FR-RWB-010` / RWB-E1-042 (`aisdlc/requirement/Traceability_Matrix.md` lines 33 and 51) and the story file v7 [S-01]; REQ-DRI-010 (story v7 §18) |
| Code base | This repository (`<repo>`), platform baseline `751909e`. Nothing from the v2 spec's ACE monorepo layout is assumed |
| Supersedes | `_v2-baseline/specify/spec.md` (16 Nov 2026). What still holds is reused; every change is mapped by finding in `gate-response.md` |
| Status | SUCCESS_WITH_ASSUMPTIONS: every rule is mapped; open items carry labelled assumptions (`assumptions.md`); none blocks planning |

Path abbreviations: `legacy/` is `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/`.
`aisdlc/`, `api/` and `backend/` paths are under `<repo>`. Line numbers are as read on 17 Nov 2026.

## 1. Sources

| ID | Document (name, version, section) | Path |
|---|---|---|
| S-01 | User Stories Epic 1 Story Files v7, RWB-E1-042 | `legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-042-central-configuration-service-and-parameter-catalog-v1.md` |
| S-02 | Increment card INC-003 | `aisdlc/docs/increments/INC-003-epic-1-RWB-E1-042.md` |
| S-03 | Decision Log v10, D-RCV-28 (migration naming, `${recoverySchema}`) | `legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` line 77 |
| S-04 | Temporal and Drools Change Register v1 (D-RCV-36), §3.1 | `legacy/16-temporal-and-drools-adoption/recovery-workbench-temporal-and-drools-change-register-v1.md`; working copy `aisdlc/docs/decisions/d-rcv-36-temporal-and-drools.md` lines 78-87 |
| S-05 | Physical Schema v6 | `legacy/06-data/recovery-workbench-physical-schema-v6.sql` (parameter_catalog 1386-1409, parameter_value 1412-1434, reference_version 1437-1467, outbox_event 1206-1225) |
| S-06 | API Specification v4 | `api/recovery-api-v4.yaml` (postAdminReferenceLoads 3167, approve 3214, verify 4961, getAdminParameters 4857, rollback 5004; schemas Parameter, ReferenceLoad, RollbackRequest, Problem) |
| S-07 | Users, Roles and Permissions v4, matrix sheet | `legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v4-xlsx.md` lines 73-110 |
| S-08 | Error and Message Standard v4 | `legacy/07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` (Thai status line 19; storage line 56; message rows 68-207) |
| S-09 | RWB-E1-042 Clarification Pack, 10 Nov 2026 ("For review") | `legacy/e1-042-migration-and-clarifications/rwb-e1-042-clarification-pack.md` (same text in `<docset>/E1-042 Migration and Clarifications/`) |
| S-10 | Story files v7, RWB-E1-043 | `legacy/04-user-stories/.../rwb-e1-043-reference-data-service-with-versioned-tables-v2.md` |
| S-11 | Story files v7, RWB-E1-045 | `legacy/04-user-stories/.../rwb-e1-045-multi-product-parameters-for-mortgage-hp-and-ssme-v1.md` |
| S-12 | Build Sequence Epic 1 and Epic 2 v6 | `legacy/11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md`; working copy `aisdlc/docs/increments/build-sequence.md` |
| S-13 | Event and Messaging Design v4 | `legacy/05-technical-architecture/recovery-workbench-event-and-messaging-design-v4.md` |
| S-14 | Run decisions D-RUN-07 (migration numbers), D-RUN-08 (dependencies), D-RUN-10 (reference-load endpoint owned by RWB-E1-043), D-RUN-11 (handler map published by RWB-E1-043) | `AI-SDLC-BUILD-LOG.md` lines 29, 30, 33, 34; `aisdlc/RUN-BRIEF.md` |
| S-15 | Phase 0 standards audit, A-01, A-03, A-04, A-06, A-08 | `aisdlc/evidence/phase0-standards-audit.md` |
| S-16 | Repository code (platform baseline) | `backend/...` paths cited inline |
| S-17 | Recovery Workbench AI engineering standards v2 | `AGENTS.md` |
| S-18 | Repository README, "Decisions taken while setting this up", items 1 and 5 | `README.md` |
| S-19 | Spec gate review `REVIEW-RWB-E1-042-SPEC-003` | `aisdlc/output/INC-003-epic-1-RWB-E1-042/review/spec-gate-review.md` |
| S-20 | v2 build pack (13-row catalog, messages CSV, 10 Nov SQL), reused as input | `aisdlc/output/INC-003-epic-1-RWB-E1-042/_v2-baseline/implement/` |

## 2. Change Scope Declaration

| Item | Value |
|---|---|
| Change Type | `NEW_STORY`. No parameter code exists in this repository: `backend/src/main/java/.../recovery/` holds only the platform, rules, workflow and documents skeletons, and the migration folder is empty [S-16]. The card's "Implemented" status describes the ACE monorepo pack, not this repository [S-02] |
| UI In Scope | NO. Story v7 §15: "No screen in this story"; SCR-39 is Epic 8 [S-01] |
| Logic In Scope | YES |
| API In Scope | YES (one endpoint: `GET /admin/parameters`) |
| API Impact Type | `NEW_API_REQUIRED` for the code base: `GET /admin/parameters` is implemented for the first time. The OpenAPI file already holds it [S-06]; this spec makes **no change** to `api/recovery-api-v4.yaml`. The three reference-load operations are **not** exposed by this story (D-RUN-10): RWB-E1-043 owns the endpoint and calls this story's published `ParameterLoadHandler` (§11.2). One new internal event is declared as a delta (§11.4) |
| Impacted Existing Nodes | `platform` module: `RecoveryFlags`, `RecoveryProperties`, `PlatformConfig`, `ApiProblemException`, `ProblemFactory`, `ApiExceptionHandler` (additive); `application.yaml`, `application-local.yaml`; `backend/build.gradle.kts` (key generation task); `RecoveryMigrationLintTest` (unchanged; the new file must pass it) |
| New Nodes Required | YES: configuration service in the `platform` module, one migration, the catalog file, two build checks, tests |
| Inherited Existing Behavior | Recovery Flyway bean with the `recoverySchema` placeholder (`RecoveryFlywayConfig.java:37`); migration lint (`RecoveryMigrationLintTest.java:25, 82-84, 94-95`); RFC 7807 Problem through `ProblemFactory` / `ApiExceptionHandler` (README decision 1); `SecurityConfig` JWT resource server with 401 `MSG-P4-001` for a caller with no RW- role; readiness probes (`application.yaml`, `management.endpoint.health.probes`); Testcontainers PostgreSQL 16 tests (`recoveryIntegrationTest`, tag `recovery-it`) [S-16] |
| Frontend Changes Required | NO |
| Backend Changes Required | YES |

## 3. User story intent interpretation

As a squad member (RW-TRIBE), I want every environment setting and business parameter read from one
configuration service and listed in a catalog with name, type, default, owner, environment and where it
is used, so that a value changes by a checked, approved, dated load and not by a release [S-01 §1, §2].

In this repository that means:

1. A catalog file in the repository is the only place a parameter is defined. The build turns it into
   typed keys, and two build checks stop literals and uncatalogued keys (BR1, BR2).
2. One migration creates (or completes) the two parameter tables and seeds the catalog and version 1 of
   every default (story §4 step 4).
3. `ParameterService` (published in `platform.api`) returns a typed value with its version for a business
   date, per environment, with no restart when a new version starts (BR5, AC11).
4. `ParameterLoadHandler` (published in `platform.api`) validates and applies a `PARAMETER` load, its
   approval by a different person, and its rollback (BR3, BR4). RWB-E1-043's shared reference-load
   endpoint calls it (D-RUN-10); until then nothing exposes it over HTTP.
5. Secrets are listed, never served (BR6). The service is not ready while a required parameter has no
   value and no default (BR7).
6. Work owned by later stories (the reference-load endpoint, decision log, outbox, permission matrix,
   sessions, flag table, ACE business date, message table) is reached through a named seam (§4.3).

## 4. Entry triggers and preconditions

### 4.1 Triggers

| Trigger | Actor | Path |
|---|---|---|
| Catalog change merged | Squad member through reviewed PR; owner reviews [S-01 §4 step 1] | Build (key generation, checks). A new key also needs a migration in the story that adds it |
| Deployment | Flyway (recovery bean) | Migration creates or completes tables and seeds (story §4 step 4) |
| Start-up and every readiness probe | Kubernetes / Spring Boot | `ParameterStartupCheck` (SPEC-016) |
| Value load, approval, rollback | RW-COE or RW-REFADM loads; an approver who is not the author approves; a holder of Reference data U rolls back [S-01 §3, §12] | RWB-E1-043's endpoint calls `ParameterLoadHandler` (SPEC-017). In this story: called in tests only |
| Read | Recovery code (through `ParameterService`); any role with Rules and parameters R (through `GET /admin/parameters`) | SPEC-007, SPEC-011 |

### 4.2 Preconditions (story v7 §3) and how this repository meets them

| # | Precondition [S-01 §3] | In this repository |
|---|---|---|
| PRE-1 | RWB-E1-044 done: the recovery schema exists | The recovery Flyway bean, the placeholder and the lint exist (phase0 A-04). Locally the schema is built from Physical Schema v6 when `RWB_LOAD_REFERENCE_SCHEMA=true` (README); the migration also runs on an empty schema (SPEC-001) |
| PRE-2 | `config/parameter-catalog.csv` in the repository, owned by RW-COE, with the Epic 1 entries incl. `case.entry.dpd` 90, `refdata.cache.ttl-seconds` 300, `caselist.export.maxrows` 10000 | Not present. This story adds it with the 19-row bootstrap set in §12.4 (13 rows from the 10 Nov pack [S-20] plus the six D-RCV-36 keys [S-04]). The full Epic 1 file is absent from the document set (OI-E1-042-003, CLAR-003) |
| PRE-3 | The secret store holds secrets; the catalog lists them only | Rows with `secret=true` have no default and no value row (DB check, SPEC-002); values come from the environment / Key Vault as today (`application.yaml` header comment) |
| PRE-4 | Loaders hold Reference data C (RW-COE, RW-REFADM); approvers hold Reference data A (owner; RW-RISK assumed, DL01) | Enforced on the endpoint, which is RWB-E1-043's (D-RUN-10). Users, Roles and Permissions v4 grants Reference data CRUD to RW-COE and RW-REFADM; **no role** holds Reference data A [S-07 lines 101, 107; S-06 line 3232]. Recorded as CLAR-013 for RWB-E1-043 and RWB-E1-037. This story enforces maker-checker inside the interface regardless of role |
| PRE-5 | The pipeline runs this story's checks on every PR | Both checks are JUnit tests in the `test` task, which `check` runs (SPEC-003, SPEC-004) |

### 4.3 Dependencies and seams (D-RUN-08, D-RUN-10)

Only RWB-E1-044 (order 1) and RWB-TE-001 (order 2) precede this story [S-12]. Everything else is a seam:
this story builds the interface and, where needed, an interim implementation; the later story fills it
without changing callers.

| Later work | Owner (order) | What RWB-E1-042 builds now | How the seam is filled later |
|---|---|---|---|
| Shared reference-load endpoint (`POST /admin/reference-loads`, `/{loadId}/approve`, `/{loadId}/rollback`), dispatch by table code, capability checks C/A/U, `/verify`, LOV-REF-TABLE | RWB-E1-043 (8), D-RUN-10, D-RUN-11 | The published `ParameterLoadHandler` interface (load, approve, rollback, find) with all `PARAMETER` validation, versioning, maker-checker, idempotency and refusals as `ApiProblemException` (SPEC-017). **No controller** | RWB-E1-043's `PARAMETER` branch calls `ParameterLoadHandler`, maps the HTTP request to it and returns its result; its own handler map (D-RUN-11) may wrap it. Until RWB-E1-043 merges, nothing exposes the endpoint |
| Decision log entry `AC-VERS` on approval (API v4 line 3233) | RWB-E1-008 (12) store, RWB-E1-027 (20) writer | `VersionDecisionRecorder` interface, called once per approval; interim implementation writes one structured log line with no personal data (SPEC-019) | RWB-E1-027 provides the implementation that writes the decision log entry |
| Outbox publication of `ParameterVersionApproved` | RWB-TE-006 (23) | In-process Spring application event after commit, plus the cache TTL (SPEC-018) | RWB-TE-006 adds the outbox write in the same transaction. Note: `outbox_event.case_seq` is nullable and `UNIQUE (case_seq, idempotency_key)` does not de-duplicate rows with null `case_seq` [S-05 1206-1225] |
| Capability check from the permission matrix; real sessions | RWB-E1-037 (27), RWB-E1-022 (26); contract lint RWB-TE-003 (5) | `CapabilityCheck` interface used by the method check on `GET /admin/parameters`, naming area and right; interim implementation reads a grants file for Rules and parameters derived from Users, Roles and Permissions v4 (SPEC-020) | RWB-E1-037 replaces the implementation and deletes the file. TC-E1-042-12 runs then (OI-E1-042-001) |
| Flag table with removal date | RWB-E1-047 (16) | Flag `rwb.p3.configservice` in the `RecoveryProperties` / `RecoveryFlags` / `@ConditionalOnProperty` pattern (SPEC-021) | RWB-E1-047 moves the flag to its table |
| ACE business date (`v_ace_batch_status`) | RWB-E1-069 (10) views; read by RWB-E1-043 [S-10 line 45] | `BusinessDateProvider` interface; interim implementation: today's date in Asia/Bangkok (SPEC-023) | The story that reads the batch-status view replaces the implementation |
| Message table | None assigned (OI-E1-042-004) | `MessageResolver` with a fixed catalog of this story's messages, EN and TH (SPEC-022) | A message-table story swaps the implementation |
| Product parameter values (PRODUCT scope) | RWB-E1-045 (31) | Catalog rows only; loads of PRODUCT keys are refused (SPEC-012) | `ProductParameterService` of RWB-E1-045 |
| Readers switching to `ParameterService` (Temporal, Drools) | RWB-E1-071 (35), RWB-E1-072 (36) | Catalog entries with value source ENV for the existing `rwb.*` properties (SPEC-024) | Those stories change their own modules' reads |

## 5. SPEC catalogue

Every SPEC item traces to `FR-RWB-010` (Traceability Matrix line 33). Tests are in §15.

| SPEC ID | Statement | Source | Tests |
|---|---|---|---|
| SPEC-RWB-E1-042-001 | Exactly one migration file `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` in `backend/src/main/resources/db/modulemigration/recovery/`; `<seq>` is the next free four-digit number at merge, assigned by the orchestrator, never fixed in this spec or the plan. Line 1 is `-- Story: RWB-E1-042`. DDL and seed are in this one file. Only `${recoverySchema}` qualifies objects; no `SET search_path`; no GRANT or REVOKE. All DDL is guarded, so it runs on an empty schema and on a schema already built from Physical Schema v6 | D-RCV-28 [S-03]; D-RUN-07 [S-14]; `RecoveryMigrationLintTest.java:25, 82-84, 94-95`; story v7 §4 step 4, §13 | TC-13, TC-14, TC-15 |
| SPEC-RWB-E1-042-002 | Table shapes follow Physical Schema v6 (`id uuid` PK; `uk_parameter_catalog UNIQUE (param_key)`; `uk_parameter_value`). This story **adds** the columns `parameter_value.load_id uuid`, `content_hash char(64)` and `rollback_reason varchar(400)`; FK `fk_parameter_value_catalog`; the check constraints and indexes of §12.3. A Physical Schema update request is raised (shared-updates.md) | S-05 1386-1434, 1437-1467; story v7 §13 (FK, partial index); pack §3.7 option A; findings 104, 112 | TC-13, TC-14, TC-27 |
| SPEC-RWB-E1-042-003 | `CatalogCompletenessCheck` fails the build naming every key read in recovery main code that the catalog lacks, and every catalog row with no owner, an invalid kind, type or scope, an invalid range, or no default. The default rule exempts `scope=PRODUCT`, `secret=true` and `value_source=ENV` rows; owner, type and range are still required | AC3, BR2; story §13 components; OI-E1-042-007 | TC-03, TC-21 |
| SPEC-RWB-E1-042-004 | `RwbMagicNumberCheck` fails the build on a numeric literal other than 0, 1, -1 in recovery main code, and on a string literal equal to a non-secret catalog default; each finding names the file, the line and the catalog key(s) whose default equals the literal. Test code and generated code are excluded. Literals already in the baseline code are listed in a reviewed baseline file; an unlisted literal or a stale entry fails (ratchet) | AC2, BR1; story §13 components; finding 108 | TC-02, TC-25 |
| SPEC-RWB-E1-042-005 | A Gradle task generates `ParameterKeys` (one typed `ParameterKey<T>` constant per catalog row, carrying type, scope, secret flag, value source, property name and default) from the catalog file before `compileJava`. Code reads a value only through `ParameterService` with a generated key | Story v7 §4 step 2, §13 `ParameterKeysGenerator`; pack §4 | TC-26, TC-27 |
| SPEC-RWB-E1-042-006 | The migration seeds every catalog row of §12.4 and, for every GLOBAL, non-secret, `value_source=TABLE` row with a default, one value row per listed environment: version 1, `APPROVED`, `valid_from = 2026-11-02`, author = seed identity `00000000-0000-0000-0000-0000000e1042`, approver NULL, `approved_at = now()`, `load_id` NULL. A self-check in the same file raises an exception if a required GLOBAL non-secret row with a default lacks an approved value for a listed environment | Story v7 §3, §4 step 4, §13; finding 110; assumptions A-04, A-05 | TC-01, TC-13, TC-14, TC-27 |
| SPEC-RWB-E1-042-007 | `ParameterService.get(key, businessDate)` returns `ParameterValue<T>(key, value, versionNo, validFrom, environment)` for the running environment: the `APPROVED` row for (key, environment, product group NULL) with the latest `valid_from` on or before the business date. If none is in force it returns the catalog default with `versionNo = 0` and `validFrom = null`; with no default it throws `ParameterNotInForceException` | AC1, BR1, BR5; story §12 interface; S-08 MSG-P3-027 ("no version is in force for a table an engine needs") | TC-01, TC-11 |
| SPEC-RWB-E1-042-008 | The environment is `rwb.environment` (DEV, SIT, UAT, PROD). The same key resolves independently per environment | AC8; `application.yaml` `rwb.environment` | TC-08 |
| SPEC-RWB-E1-042-009 | Each instance caches, per (key, environment), the ordered list of approved versions; the date is resolved on read, so a version starts on its `valid_from` with no restart and no refresh. Entries expire after `config.cache.ttl-seconds` (default 60) and are rebuilt on `ParameterVersionApproved` and on a local rollback | AC11, BR5; story §4 step 8, §13 (TTL 60, DL11) | TC-11, TC-28 |
| SPEC-RWB-E1-042-010 | A `secret=true` key is never served: `ParameterService.get` throws `SecretNotServedException`; `GET /admin/parameters` lists the entry (owner, environments, used by) with `valueInForce`, `default`, `versionNo` and `validFrom` absent; no secret value is in a table, log or response | AC9, BR6, X7; story §17 | TC-09 |
| SPEC-RWB-E1-042-011 | `GET /api/recovery/v1/admin/parameters` returns the catalog with the value in force per environment (filters: key prefix, kind, owner, environment); method check Rules and parameters R through `CapabilityCheck` | Story §12; API v4 getAdminParameters | TC-09, TC-31, TC-24, TC-12 (blocked) |
| SPEC-RWB-E1-042-012 | `ParameterLoadHandler.load` takes CSV `key,environment,value` with `validFrom` and the author's user ID; every row is checked (catalog key, loadable key, environment, non-empty, type, range, no duplicate); `validFrom` is not before the business date; the load is refused whole on the first failure; on success every row is written `VALIDATED` with the next version number for its (key, environment), the author, and one `load_id` | AC5, AC6, BR3, X4, X5; story §4 step 6, §12; pack §3.3, §3.6; RWB-E1-043 X3 | TC-05, TC-06, TC-23 |
| SPEC-RWB-E1-042-013 | Idempotency key `(PARAMETER, validFrom, content_hash)`; hash = SHA-256 over the canonical rows (§12.6), stored in `parameter_value.content_hash`. An identical repeat of a load that is `VALIDATED` or `APPROVED` returns the existing load marked `repeat = true` and writes nothing (the endpoint answers 201 with the same body, OI-E1-042-011). Different content for a (key, environment) that already has an `APPROVED` version on or after `validFrom` is refused with 409 MSG-P3-027 | Story §12 idempotency; pack §3.6; RWB-E1-043 X4 | TC-16, TC-17 |
| SPEC-RWB-E1-042-014 | `ParameterLoadHandler.approve(loadId, approverUserId)`: all rows must be `VALIDATED`; the approver must not be the author (409 MSG-P7-002, also a DB check); rows become `APPROVED` with approver and time; `valid_to` is recomputed for each affected (key, environment); one `VersionDecisionRecorder` call; one `ParameterVersionApproved` after commit; a concurrent or repeated approval gets 409 MSG-GEN-004 | AC7, BR4, X6; story §9, §12; API v4 approve; RWB-E1-043 X5 | TC-07, TC-20, TC-29 |
| SPEC-RWB-E1-042-015 | `ParameterLoadHandler.rollback(loadId, reason, userId)`: `reason` non-blank, at most 400 characters; only an `APPROVED` load; every row must have an earlier `APPROVED` version of its (key, environment), else 409 MSG-P3-015 and nothing changes; rows become `ROLLED_BACK` with the reason; `valid_to` is recomputed so the earlier version is in force again | AC10, X8; story §9, §12; API v4 rollback (`RollbackRequest`) | TC-10, TC-18, TC-19 |
| SPEC-RWB-E1-042-016 | `ParameterStartupCheck` is a health indicator in the readiness group. It is DOWN, with MSG-P3-032 naming each key and the environment, when a required GLOBAL non-secret key listed for the running environment has neither an `APPROVED` value row (any `valid_from`) nor a catalog default (TABLE source), or its property does not resolve (ENV source). `valid_from` is not consulted, so a future-dated seed never fails readiness | AC4, BR7, X3; story §13; triage decision (f); finding 110 | TC-04 |
| SPEC-RWB-E1-042-017 | `ParameterLoadHandler` is published in `platform.api` with `load`, `approve`, `rollback` and `find(loadId)`, returning `ParameterLoadResult(loadId, table "PARAMETER", validFrom, status, rows, repeat)`. Refusals are thrown as `ApiProblemException` carrying the message ID, HTTP status, placeholders and field of §10.2, so the caller's controller renders them unchanged. An unknown `loadId` throws 404. This story builds no controller for these operations (D-RUN-10) | Story §12 ("this story builds the PARAMETER handler"), §13 `ParameterLoadHandler`; D-RUN-10, D-RUN-11; AGENTS §3.11; finding 103(a) | TC-05, TC-07, TC-10, TC-23 |
| SPEC-RWB-E1-042-018 | Event `ParameterVersionApproved` (delta, §11.4) is published as an in-process application event after the approval commits; listeners in the same instance rebuild the cache. The outbox write is RWB-TE-006's | Story §12 event; findings 103(b), 116 | TC-28 |
| SPEC-RWB-E1-042-019 | Every approval calls `VersionDecisionRecorder.recorded(decisionCode "AC-VERS", table "PARAMETER", loadId, keys, validFrom, approverUserId)`; the interim implementation logs one structured line without the approver ID | API v4 approve ("decision log entry with decision code AC-VERS"); finding 103(c) | TC-29 |
| SPEC-RWB-E1-042-020 | The endpoint this story exposes has a method check naming the capability area and right through `CapabilityCheck`; a refusal is 403 MSG-P4-002 with action "read parameters". The interim implementation reads `backend/src/main/resources/platform/interim-capability-grants.csv` (§12.10) | AGENTS §3.3; API v4 `x-capability`; S-07; findings 103(d), 114, 118 | TC-24, TC-12 (blocked) |
| SPEC-RWB-E1-042-021 | Flag `rwb.p3.configservice` (default `false`; `true` in the local profile). Off: `ParameterService` serves catalog defaults from the generated keys (`versionNo 0`) and ENV values with no database read; `GET /admin/parameters` is not registered (404); the `ParameterLoadHandler` bean is not registered, so loads cannot be applied ("value loads are refused") | Story §13 feature flag; D-RCV-36 flag rule ("endpoints return 404"); AGENTS §3.13 | TC-22 |
| SPEC-RWB-E1-042-022 | Story messages are resolved by message ID through `MessageResolver` (platform.api); the interim `FixedMessageCatalog` holds EN and TH text from Error and Message Standard v4 for the IDs in §10.3. `ProblemFactory` fills `messageCode`, `messageTh`, `detail` and `field` | AGENTS §3.6; S-08; README decision 5; pack §6.2; finding 109 | TC-30 |
| SPEC-RWB-E1-042-023 | The business date for the load check and for `GET /admin/parameters` comes from `BusinessDateProvider`; interim: the current date in Asia/Bangkok. `ParameterService` callers pass their own business date | Story §12 interface; RWB-E1-043 §3 line 45; `application.yaml` time zone | TC-23, TC-11 |
| SPEC-RWB-E1-042-024 | The six D-RCV-36 keys are catalog rows (§12.4). `temporal.target`, `temporal.namespace` and `drools.kiebase.cache.max` have `value_source=ENV`, naming the existing properties `rwb.temporal.target`, `rwb.temporal.namespace`, `rwb.drools.kiebase-cache-max`; their readers are unchanged in this story | D-RCV-36 §3.1 [S-04]; story §13 ("Environment settings come from the environment"); phase0 A-06; finding 108 | TC-26, TC-27 |
| SPEC-RWB-E1-042-025 | Errors are RFC 7807 `Problem` bodies (type, title, status, detail, messageCode, messageTh, field, traceId) as in §10.2, raised through `ApiProblemException` | API v4 Problem; README decision 1 | TC-05, TC-06, TC-07, TC-10, TC-18, TC-19, TC-23, TC-30 |
| SPEC-RWB-E1-042-026 | All code is in the `platform` module: published types in `th.co.scb.ace.demo.recovery.platform.api`, implementation in `...platform.internal.parameter`. Other modules use only `ParameterService` and `ParameterLoadHandler` | AGENTS §3.11, §7 (one module); story §13 package; plan input 5; assumption A-01 | Existing `ModulithTest`, `RecoveryBoundaryTest` |
| SPEC-RWB-E1-042-027 | No personal data: synthetic UUIDs only in seed, fixtures and tests; no names or IDs in logs; no secret value anywhere; author and approver are user UUIDs (DF-REF-156, not personal) | Story §17; AGENTS §4.7; S-05 DF-REF-132..158 `is_personal=false` | TC-09, TC-29, code review |

## 6. Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every changeable business value is a versioned parameter row, never a constant | 004, 005, 006, 007 | DIRECT | Literal check, generated keys, seeded version 1 | COVERED |
| BR2 | Every parameter in use has a catalog entry with owner, type, default, environments, used by | 003, 005 | DIRECT | PRODUCT, secret and ENV rows are exempt from the default rule only | COVERED |
| BR3 | A business value changes only through a checked, approved, dated load | 012, 013, 014, 015 | DIRECT | The seed is the reviewed-PR baseline, not a change (A-05) | COVERED |
| BR4 | Author cannot approve; Risk approves where a threshold or limit moves | 014 | DIRECT | Author rule in service and DB. Who holds Reference data A is decided on RWB-E1-043's endpoint and RWB-E1-037's matrix (CLAR-013) | COVERED |
| BR5 | Open decisions keep their version; new decisions use the version in force | 007, 009 | DIRECT | Every read returns `versionNo`; callers record it | COVERED |
| BR6 | Secrets listed in the catalog, held only in the secret store | 010, 002 | DIRECT | `ck_parameter_catalog_secret_default`; no value rows for secrets | COVERED |
| BR7 | A service does not start without every required parameter for its environment | 016 | DIRECT | Readiness DOWN, no traffic (AC4 wording) | COVERED |
| AC1 | `case.entry.dpd` = 90 PROD v1; read on 2026-12-01 gives 90 and version 1 | 006, 007 | DIRECT | Seed v1 from 2026-11-02. Recording version 1 in the entry decision is the case service's (RWB-E1-018) | COVERED |
| AC2 | Literal 90 in `recovery.casewf.casecreation` fails the build naming file, line, `case.entry.dpd` | 004 | DIRECT | Fixture module (story §13 build step 7) | COVERED |
| AC3 | Code reading `allocation.retry.limit` not in the catalog fails the build naming it; every other key in use is catalogued with owner and default | 003 | DIRECT | Fixture module | COVERED |
| AC4 | Required `refdata.cache.ttl-seconds` with no value and no default in UAT: health fails with MSG-P3-032 naming key and UAT; no traffic | 016, 022 | DIRECT | Readiness group | COVERED |
| AC5 | Load `case.entry.dpd` = 400 PROD refused with MSG-GEN-002 min 1 max 365 | 012, 025 | DIRECT | 422 through the interface | COVERED |
| AC6 | Load "ninety" refused with MSG-P1-002, check "value is not INTEGER" | 012, 025 | DIRECT | 422 through the interface | COVERED |
| AC7 | U-41 loaded version 3 and approves it: refused MSG-P7-002 | 014 | DIRECT | 409; DB check as second guard | COVERED |
| AC8 | `refdata.cache.ttl-seconds` 30 in SIT, 300 in PROD; each environment reads its own | 008, 012, 014 | DIRECT | Table values for an ENVIRONMENT-kind key (CLAR-014) | COVERED |
| AC9 | `ace.db.password` listed with owner, environments, used by; no value returned | 010, 011 | DIRECT | | COVERED |
| AC10 | Version 2 in force, version 1 before it; rollback of v2 makes v1 in force, 90 | 015 | DIRECT | | COVERED |
| AC11 | v2 = 91 PROD from 2026-12-10 approved 2026-12-05: 90 on 12-09, 91 on 12-10, no restart | 007, 009, 014 | DIRECT | Date resolved on read | COVERED |
| X1 | Literal business value: build fails naming file, line, parameter | 004 | DIRECT | | COVERED |
| X2 | Uncatalogued key: build fails naming it | 003 | DIRECT | | COVERED |
| X3 | Required value missing at start-up: not started; health names key; MSG-P3-032 | 016 | DIRECT | "Not started" read as readiness DOWN per AC4 (CLAR-012) | COVERED |
| X4 | Out of range: load refused in full, MSG-GEN-002 | 012 | DIRECT | | COVERED |
| X5 | Wrong type: load refused in full, MSG-P1-002 | 012 | DIRECT | | COVERED |
| X6 | Approver is author: refused, MSG-P7-002 | 014 | DIRECT | | COVERED |
| X7 | Secret asked for through the catalog read: no value | 010 | DIRECT | | COVERED |
| X8 | Rollback: previous version in force; MSG-P3-015 when none | 015 | DIRECT | | COVERED |
| X9 | Role without Rules and parameters R reads the catalog: 403 MSG-P4-002 | 011, 020 | DIRECT | TC-12 Blocked until RWB-E1-022 and RWB-E1-037 (OI-E1-042-001); seam test TC-24 does not close it | COVERED |
| X10 | Version approved before its valid from: current value stays until then; no restart | 009, 014 | DIRECT | | COVERED |
| FL1 | Squad member adds a catalog row through a PR reviewed by the owner | 003, 005 | INHERITED_EXISTING_BEHAVIOR | Merge review (AGENTS §8); CODEOWNERS is RWB-TE-002 | COVERED |
| FL2 | Build generates `ParameterKeys`; code reads only through `ParameterService` | 005, 007 | DIRECT | | COVERED |
| FL3 | Build runs the magic-number and completeness checks | 003, 004 | DIRECT | | COVERED |
| FL4 | Flyway loads catalog rows and defaults | 001, 006 | DIRECT | | COVERED |
| FL5 | RW-COE loads a value version through reference-loads, table PARAMETER | 012, 017 | DIRECT | HTTP path is RWB-E1-043's endpoint calling `ParameterLoadHandler` (D-RUN-10) | COVERED |
| FL6 | Load checks key, type, range, environment, required values; refuse whole | 012 | DIRECT | "Required values": a blank value is refused (MSG-GEN-001) | COVERED |
| FL7 | Owner approves; refused if approver is author | 014 | DIRECT | | COVERED |
| FL8 | New value from valid from; every instance refreshes on the event or after the TTL | 009, 018 | DIRECT | Cross-instance refresh relies on the TTL until RWB-TE-006 | COVERED |
| FL9 | Engines read with version number and record it in decision inputs | 007 | DIRECT | Recording belongs to the engines' stories | COVERED |
| FL10 | Any role with Rules and parameters R reads the catalog through GET | 011, 020 | DIRECT | | COVERED |
| PRE1-PRE5 | Story §3 preconditions | §4.2 | DIRECT | | COVERED |
| ST1 | None -> Load (all checks pass) -> VALIDATED | 012 | DIRECT | | COVERED |
| ST2 | VALIDATED -> Approve (approver is not author) -> APPROVED, in force from valid from | 014 | DIRECT | | COVERED |
| ST3 | APPROVED -> Rollback (earlier approved version exists) -> ROLLED_BACK | 015 | DIRECT | | COVERED |
| AUTH | Story §10 authority (RW-COE, RW-RISK, RW-PLATADM, RW-TRIBE, readers, RW-PHONECOL) plus RW-REFADM as loader (§3) | 020, 014, §16 | DIRECT | Load/approve/rollback rights are checked on RWB-E1-043's endpoint | COVERED |
| CON1 | GET /admin/parameters contract | 011 | DIRECT | | COVERED |
| CON2 | POST reference-loads PARAMETER contract incl. idempotency | 012, 013, 017 | DIRECT | Through the published interface | COVERED |
| CON3 | Approve and rollback contracts | 014, 015, 017 | DIRECT | Through the published interface | COVERED |
| CON4 | Event ParameterVersionApproved | 018 | DIRECT | Payload delta §11.4 | COVERED |
| CON5 | Published interface `ParameterService`, `ParameterValue`, `ParameterKeys` | 005, 007, 026 | DIRECT | Package mapped to this repository (A-01) | COVERED |
| MSG | Story §14 messages (7) plus MSG-P4-001 | 022, 025 | DIRECT | §10.3 | COVERED |
| GR1 | No business value in code | 004 | DIRECT | | COVERED |
| GR2 | No personal data; no secret value in tables, logs, responses | 010, 027 | DIRECT | | COVERED |
| GR3 | No read of another module's tables; values only through ParameterService | 026 | INHERITED_EXISTING_BEHAVIOR | Modulith verification and the boundary test | COVERED |
| GR4 | A value change needs no deployment; a new parameter needs a reviewed catalog entry | 009, 012, 003 | DIRECT | | COVERED |

## 7. Field-level behavior matrix

### 7.1 Catalog file `backend/src/main/resources/config/parameter-catalog.csv` (build time; changed by PR only)

Header: `key,kind,value_type,unit,min_value,max_value,default_value,scope,required,owner_role,environments,used_by,secret,value_source,env_property,description`.
The first 13 columns and `description` are the 10 Nov pack header [S-20]; `value_source` and
`env_property` are added (story §6, "catalog columns ... can be tuned"; story §13 environment settings; A-03).

| Column | Constraint (checked by `CatalogCompletenessCheck`) | Maps to |
|---|---|---|
| key | Required, unique, `^[A-Za-z][A-Za-z0-9_.-]{0,99}$` | `param_key` |
| kind | `BUSINESS` or `ENVIRONMENT` | `kind` |
| value_type | STRING, INTEGER, DECIMAL, BOOLEAN, DATE, TIME, DURATION, CODE, CODE_LIST or JSON | `value_type` |
| unit | Optional, max 20 | `unit` |
| min_value, max_value | Optional; when present they parse as `value_type`; min <= max | `min_value`, `max_value` |
| default_value | Required except when scope=PRODUCT, secret=true or value_source=ENV; parses and lies in range; empty when secret=true | `default_value` |
| scope | `GLOBAL` or `PRODUCT` | `scope` |
| required | `true` or `false` | `required` |
| owner_role | Required; an RW- role code of Users, Roles and Permissions v4 | `owner_role` |
| environments | Comma list of DEV, SIT, UAT, PROD | `environments` |
| used_by | Free text, max 400 | `used_by` |
| secret | `true` or `false`; `true` requires value_source=SECRET | `secret` |
| value_source | `TABLE`, `ENV` or `SECRET` | Generated key only (not a DB column) |
| env_property | Required when value_source=ENV: the Spring property; empty otherwise | Generated key only |
| description | Required, max 400 | `description` |

### 7.2 `parameter_catalog`

All columns as Physical Schema v6 lines 1386-1409; written by migrations only, never at run time.
`created_by` of seeded rows = seed identity. Editable through the API: none.

### 7.3 `parameter_value`

| Field | On load | On approve | On rollback | Constraint |
|---|---|---|---|---|
| id | `gen_random_uuid()` | | | PK (v6) |
| param_key | CSV `key` | | | FK to `parameter_catalog.param_key` (added) |
| environment | CSV `environment` | | | DEV, SIT, UAT, PROD (check added) |
| param_value | CSV `value`, trimmed | | | NOT NULL, max 400 |
| product_group | NULL (PARAMETER loads are GLOBAL) | | | |
| version_no | max(version_no) of (key, environment, product_group NULL) + 1, over all statuses | | | >= 1; unique with `ux_parameter_value_version_all` |
| valid_from | `validFrom` | | | |
| valid_to | NULL | recomputed (§12.7) | recomputed | NULL or >= valid_from |
| status | `VALIDATED` | `APPROVED` | `ROLLED_BACK` | LOV-VERSION-STATUS values (DF-REF-155) |
| author_user_id | author user ID passed by the caller (the JWT `sub` on RWB-E1-043's endpoint) | | | NOT NULL |
| approver_user_id | NULL | approver user ID | | NULL or <> author (check added) |
| approved_at | NULL | `now()` | unchanged | required when APPROVED |
| load_id (added) | one new UUID per load, on every row | | | indexed; NULL only for seeded rows |
| content_hash (added) | SHA-256 hex of the load (§12.6), on every row | | | NULL exactly when load_id is NULL |
| rollback_reason (added) | NULL | | `reason` | required when ROLLED_BACK |
| version, updated_at, updated_by | defaults | +1, now, approver | +1, now, caller | optimistic lock on `version` |

### 7.4 `ParameterLoadHandler` inputs (what RWB-E1-043's endpoint passes)

| Input | Required | Rule | Refusal |
|---|---|---|---|
| file content | Yes | UTF-8 CSV, header exactly `key,environment,value`, at least one data row | 422 MSG-GEN-001 `{field}=file` (missing or no rows); 422 MSG-P1-002 `{check}="file is not a CSV with header key,environment,value"` |
| validFrom | Yes | date, not before the business date (equal allowed) | 422 MSG-GEN-001 `{field}=validFrom`; 422 MSG-P3-027 `{check}="valid from is before the business date"` |
| author user ID | Yes | UUID | programming error (`IllegalArgumentException`) |
| loadId (approve, rollback) | Yes | UUID of a PARAMETER load | 404 MSG-P4-003 |
| approver user ID / caller user ID | Yes | UUID | programming error |
| reason (rollback) | Yes | non-blank, at most 400 characters after trim | 422 MSG-GEN-001 `{field}=reason` |

The generic P4 fields `changeRequestRef`, `impactSummary` and `rollbackPlan` (API v4 description of
postAdminReferenceLoads) are not inputs for `PARAMETER`; storing them is RWB-E2-041's (change checklist).

### 7.5 Outputs

- `ParameterLoadResult`: `loadId`, `table` = `PARAMETER`, `validFrom`, `status` (VALIDATED, APPROVED or
  ROLLED_BACK; all rows of a load share it), `rows` = number of value rows, `repeat` (true for an identical
  repeat). It maps one to one onto API v4 `ReferenceLoad` (`id`, `table`, `validFrom`, `status`, `rows`).
- `Parameter` (GET): `key`, `kind`, `type`, `unit`, `min`, `max`, `default`, `scope`, `required`, `owner`,
  `environments[]`, `usedBy[]` (split on comma), `secret`, `valueInForce`, `versionNo`, `validFrom`. For the
  requested environment (query `environment`, else `rwb.environment`) and the business date: TABLE rows give
  the value in force (or the default with `versionNo 0`); ENV rows give the property value only when the
  requested environment is the running one, else absent; PRODUCT rows and secrets have `valueInForce`,
  `versionNo` and `validFrom` absent; secrets also have `default` absent.

## 8. Status-transition matrix

| Source status | Event | Condition | Target status | Side effects |
|---|---|---|---|---|
| (none) | Load | every check passes | VALIDATED | rows written with one `load_id` |
| (none) | Load | any check fails | (nothing written) | refusal 409 or 422 |
| (none) | Load | identical repeat of a VALIDATED or APPROVED load | (unchanged) | existing load, `repeat = true` |
| VALIDATED | Approve | approver is not the author; no APPROVED row of the same (key, environment) has `valid_from` >= this load's; `validFrom` not before the business date | APPROVED | `valid_to` recomputed; decision recorder; event after commit; local cache rebuilt |
| VALIDATED | Approve | approver is the author | VALIDATED | 409 MSG-P7-002 |
| VALIDATED | Approve | `validFrom` now before the business date, or an approved version exists on or after it | VALIDATED | 409 MSG-P3-027 |
| APPROVED or ROLLED_BACK | Approve | any | unchanged | 409 MSG-GEN-004 |
| APPROVED | Rollback | every row has an earlier APPROVED version | ROLLED_BACK | `rollback_reason`; `valid_to` recomputed; local cache rebuilt |
| APPROVED | Rollback | some row has no earlier APPROVED version | APPROVED | 409 MSG-P3-015 |
| VALIDATED or ROLLED_BACK | Rollback | any | unchanged | 409 MSG-P3-027 `{check}="only an approved load can be rolled back"` |

Story v7 §9 defines VALIDATED, APPROVED and ROLLED_BACK only. IN_FORCE, SUPERSEDED and REFUSED stay allowed
by the check constraint (DF-REF-155) but are never written here; "in force" is derived from the dates.

## 9. Exceptional-case behavior

| ID | Case | Behavior | Message |
|---|---|---|---|
| X1 | Literal business value in recovery main code | `test` fails; output `path:line: literal <v> matches catalog key <key>` | build output |
| X2 | Key read but not catalogued | `test` fails naming the key and the reading file | build output |
| X3 | Required value missing for the environment | readiness DOWN; details list key and environment | MSG-P3-032 |
| X4 | Value out of range | 422, whole load refused | MSG-GEN-002 `{field}=<key>`, `{min}`, `{max}` |
| X5 | Wrong type; unknown key; key not loadable (secret, PRODUCT, ENV); environment not listed; duplicate row; bad file | 422, whole load refused | MSG-P1-002 `{source}=PARAMETER`, `{date}=<validFrom>`, `{check}` (§12.5) |
| X6 | Approver is the author | 409 | MSG-P7-002 |
| X7 | Secret read | `SecretNotServedException`; GET omits values | none |
| X8 | Rollback with no earlier version | 409, nothing changes | MSG-P3-015 `{table}=PARAMETER` |
| X9 | Caller lacks Rules and parameters R on GET | 403 | MSG-P4-002 `{action}="read parameters"` |
| X10 | Approved before valid from | old value stays until `valid_from`; no restart | none |
| E1 | Empty file, missing input, blank value | 422 | MSG-GEN-001 `{field}` |
| E2 | `validFrom` before the business date | 422 | MSG-P3-027 `{table}=PARAMETER` |
| E3 | Different content where an approved version exists on or after `validFrom` | 409 | MSG-P3-027 |
| E4 | Concurrent or repeated approval | 409 | MSG-GEN-004 |
| E5 | Rollback reason missing, blank or over 400 | 422 | MSG-GEN-001 `{field}=reason` |
| E6 | Unknown `loadId` (including seeded rows, which have no load) | 404 | MSG-P4-003 (existing `ApiError.NOT_IN_SCOPE`; text is case-oriented, CLAR-021) |
| E7 | Database unavailable on GET | 503 | MSG-GEN-006 `{system}` (pack candidate, CLAR-019) |
| E8 | Nothing in force and no default (caller read) | `ParameterNotInForceException` to the caller | MSG-P3-027 if surfaced over HTTP |
| E9 | No token or no RW- role on GET | 401 (existing `SecurityConfig`) | MSG-P4-001 |

## 10. Messages and problem mapping

### 10.1 Resolution

`MessageResolver.resolve(messageId, placeholders)` returns EN and TH text. Interim implementation
`FixedMessageCatalog` holds the IDs in §10.3. Thai text status: "Proposed": the business lead drafts and
Legal and Compliance approve (DL10) [S-08 line 19]. Where the 10 Nov pack's Thai differs from the Standard
(MSG-P4-001), the Standard v4 text is used. The Standard says messages are "held in the message table"
[S-08 line 56], and that table does not exist (OI-E1-042-004). Platform messages already in `ApiError`
(MSG-P4-001, -002, -003, MSG-P3-036) stay there (README decision 5).

### 10.2 Problem mapping

`ApiProblemException` gains an additive constructor taking a message ID, HTTP status, placeholders and an
optional `field`; `ProblemFactory` resolves the text through `MessageResolver` and sets `type`
`urn:rwb:problem:<id>`, `title`, `status`, `detail` (EN), `messageCode`, `messageTh`, `field`, `traceId`.
Existing `ApiError` behaviour is unchanged. `ParameterLoadHandler` throws these exceptions, so RWB-E1-043's
endpoint renders them through the existing `ApiExceptionHandler` with no mapping of its own.

| Status | When | messageCode | field |
|---|---|---|---|
| 401 | no token or no RW- role on GET (existing) | MSG-P4-001 | |
| 403 | GET refused by `CapabilityCheck` | MSG-P4-002, `{action}="read parameters"` | |
| 404 | unknown `loadId` | MSG-P4-003 | |
| 409 | author approves; concurrent approval; no earlier version; content conflict or approval after `validFrom`; rollback of a non-approved load | MSG-P7-002; MSG-GEN-004; MSG-P3-015; MSG-P3-027; MSG-P3-027 | |
| 422 | load and rollback validation | MSG-GEN-001, MSG-GEN-002, MSG-P1-002, MSG-P3-027 | the failing input or key |
| 503 | database unavailable on GET | MSG-GEN-006 | |

### 10.3 Message catalogue for this story (EN and TH from Error and Message Standard v4)

| ID | Used for | Placeholders | Standard v4 line |
|---|---|---|---|
| MSG-P3-032 | readiness: required parameter missing | name, environment | 156 |
| MSG-GEN-002 | value out of range | field, min, max | 69 |
| MSG-P1-002 | load refused at a check | source, date, check | 76 |
| MSG-GEN-001 | required input empty | field | 68 |
| MSG-P7-002 | approver is the author | none | 207 |
| MSG-P3-015 | no earlier version to roll back to | table | 139 |
| MSG-P3-027 | reference-data load check failed; nothing in force | table, check | 151 |
| MSG-GEN-004 | concurrent change | none | 71 |
| MSG-GEN-006 | dependency unavailable (candidate) | system | Standard v4 |
| MSG-P4-001 | 401 (added; missing from story §14) | none | 163 (existing `ApiError.NO_ROLE`) |
| MSG-P4-002 | 403 | action | 164 (existing `ApiError.NOT_PERMITTED`) |

The `{check}` and `{action}` fills are English in `messageTh` too; that is the known A-08 gap owned by
RWB-TE-003 and is not widened here.

## 11. API change assessment

### 11.1 Endpoint exposed by this story (already in API Specification v4; base path `/api/recovery/v1`)

| Method and path | operationId | Capability (x-capability) | Success | Errors | Consumer |
|---|---|---|---|---|---|
| GET `/admin/parameters` | getAdminParameters | Rules and parameters, R | 200 `Parameter[]` | 401, 403, 503 | Backend-only in this story (screen SCR-39 is Epic 8) |

### 11.2 Operations served through the published interface, exposed by RWB-E1-043 (D-RUN-10)

| API v4 operation | Capability | Endpoint owner | `ParameterLoadHandler` method | Result -> response |
|---|---|---|---|---|
| POST `/admin/reference-loads` (table `PARAMETER`) | Reference data, C | RWB-E1-043 | `load(content, validFrom, authorUserId)` | `ParameterLoadResult` -> 201 `ReferenceLoad` (also for an identical repeat) |
| POST `/admin/reference-loads/{loadId}/approve` | Reference data, A | RWB-E1-043 | `approve(loadId, approverUserId)` | -> 200 `ReferenceLoad` |
| POST `/admin/reference-loads/{loadId}/rollback` | Reference data, U | RWB-E1-043 | `rollback(loadId, reason, userId)` | -> 200 `ReferenceLoad` |
| (lookup for dispatch by `loadId`) | — | RWB-E1-043 | `find(loadId)` | `Optional<ParameterLoadResult>` |

The capability checks (C, A, U), the multipart parsing and the HTTP status of success are the endpoint's.
Every refusal comes from the interface as an `ApiProblemException` (§10.2). Until RWB-E1-043 merges these
operations are not reachable over HTTP; this story tests them through the interface (§15).

### 11.3 Contract deltas

| Delta | Kind | Action |
|---|---|---|
| None to `api/recovery-api-v4.yaml` | — | No regeneration of `frontend/src/api/schema.d.ts` |
| Identical repeat load answers 201 with the existing body; 409 only for conflicting content | Behaviour the OpenAPI leaves open | OI-E1-042-011 stays open; API owner to record it (shared-updates.md) |
| `required: [file, table, validFrom]`, `format: date`, LOV on `table` | Hardening the OpenAPI lacks | Enforced in the interface; OpenAPI change requested (OI-E1-042-011) |
| Rollback 422 = empty reason (MSG-GEN-001) | Behaviour | Recorded |
| Unknown `loadId` uses MSG-P4-003 | Behaviour | CLAR-021 |
| New published module interface `ParameterLoadHandler` | Internal Java contract | Consumed by RWB-E1-043 (D-RUN-10) |

Backward compatibility: all additive. `/platform/info` gains `flags.configservice` (an extra JSON field;
the hand-written frontend type ignores it).

### 11.4 Internal event (delta)

`ParameterVersionApproved` is new and absent from Event and Messaging Design v4 [S-13]. Producer:
`platform` (approval). Consumer now: the parameter cache of the same instance. Later: the outbox
(RWB-TE-006) and every instance.

| Field | Type | Story v7 §12 | Note |
|---|---|---|---|
| loadId | uuid | added | identifies the load |
| paramKeys | string[] | yes | |
| validFrom | date | yes | |
| versions | `[{paramKey, environment, versionNo}]` | replaces `versionNo` | one load can carry several keys and environments with different version numbers, so one `versionNo` cannot describe it |
| occurredAt | timestamp | added | |

No personal data and no approver ID in the payload. Event catalog update requested (shared-updates.md).

## 12. Backend Specification

### 12.1 Module placement (SPEC-026)

Story v7 §13 names package `recovery.casewf.config`. This repository has no `casewf` module, and the
mapping of design modules to code modules is RWB-TE-001's module map, not delivered yet (phase0 A-01, plan
input 5). The configuration service goes in the existing `platform` module, which already owns flags,
properties, Flyway, security and problem rendering. That keeps the plan to one module (AGENTS §7) and
avoids changing `ApiError` / `ProblemFactory` from another module. If RWB-TE-001's map assigns it
elsewhere, moving the package is RWB-TE-001's change (A-01).

Published (`th.co.scb.ace.demo.recovery.platform.api`): `ParameterService`, `ParameterKey<T>`,
`ParameterKeys` (generated), `ParameterValue<T>`, `CatalogEntry`, `ParameterNotInForceException`,
`SecretNotServedException`, `ParameterLoadHandler`, `ParameterLoadResult`, `ParameterVersionApproved`,
`BusinessDateProvider`, `MessageResolver`, `CapabilityCheck`, `VersionDecisionRecorder`.
Internal (`...platform.internal.parameter`): repositories, load checks, the handler implementation, the
catalog controller, cache, startup check, fixed message catalog, interim grants, interim recorder, interim
business date.

### 12.2 Published interfaces

Story v7 §12 signatures, unchanged:

```java
public interface ParameterService {
    <T> ParameterValue<T> get(ParameterKey<T> key, LocalDate businessDate);
    <T> ParameterValue<T> get(ParameterKey<T> key, String productGroup, LocalDate businessDate);
    CatalogEntry entry(String key);
}
public record ParameterValue<T>(String key, T value, int versionNo, LocalDate validFrom, String environment) {}
```

Added for D-RUN-10 (story §13 component `ParameterLoadHandler`, "approve and rollback"):

```java
public interface ParameterLoadHandler {
    String TABLE = "PARAMETER";
    ParameterLoadResult load(InputStream csv, LocalDate validFrom, UUID authorUserId);
    ParameterLoadResult approve(UUID loadId, UUID approverUserId);
    ParameterLoadResult rollback(UUID loadId, String reason, UUID userId);
    Optional<ParameterLoadResult> find(UUID loadId);
}
public record ParameterLoadResult(UUID loadId, String table, LocalDate validFrom, String status, int rows, boolean repeat) {}
```

- The product-group overload of `get` resolves a row for (key, environment, productGroup) first, then the
  GLOBAL row; this story writes no product-group rows. A `scope=PRODUCT` key throws
  `ParameterNotInForceException` (its values are RWB-E1-045's `ProductParameterService`).
- ENV-sourced keys return the converted property value, `versionNo 0`, `validFrom null`.
- Type conversion: INTEGER `Integer`, DECIMAL `BigDecimal`, BOOLEAN `Boolean` (`true`/`false`), DATE
  `LocalDate` (ISO), TIME `LocalTime` (`HH:mm`), DURATION `Duration` (ISO-8601), STRING, CODE and JSON
  `String`, CODE_LIST `List<String>` (comma-separated, trimmed).

### 12.3 Migration (SPEC-001, SPEC-002)

File `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`, adapted from the 10 Nov pack SQL [S-20]: renamed;
header cites Physical Schema v6, D-RCV-28 and this spec; `V0042` removed. Statements in order:

1. `CREATE TABLE IF NOT EXISTS ${recoverySchema}.parameter_catalog` and `parameter_value`, columns exactly
   as Physical Schema v6.
2. `ALTER TABLE ${recoverySchema}.parameter_value ADD COLUMN IF NOT EXISTS` `load_id uuid`,
   `content_hash char(64)`, `rollback_reason varchar(400)`.
3. Guarded constraint additions (`DO` blocks testing `pg_constraint` by name in `${recoverySchema}`):
   `uk_parameter_catalog` (if absent); `ck_parameter_catalog_scope` (GLOBAL, PRODUCT);
   `ck_parameter_catalog_kind` (BUSINESS, ENVIRONMENT); `ck_parameter_catalog_value_type` (§12.2 list);
   `ck_parameter_catalog_environments` (comma list of DEV, SIT, UAT, PROD);
   `ck_parameter_catalog_secret_default` (a secret has no default); `uk_parameter_value` (if absent);
   `ck_parameter_value_environment`; `ck_parameter_value_status` (VALIDATED, APPROVED, IN_FORCE,
   SUPERSEDED, ROLLED_BACK, REFUSED); `ck_parameter_value_dates`; `ck_parameter_value_version` (>= 1);
   `ck_parameter_value_maker_checker` (approver NULL or <> author); `ck_parameter_value_approved_at`
   (APPROVED and IN_FORCE need `approved_at`); `ck_parameter_value_load_hash` (`(load_id IS NULL) =
   (content_hash IS NULL)`, hash `^[0-9a-f]{64}$`); `ck_parameter_value_rollback_reason` (ROLLED_BACK needs
   a reason); `fk_parameter_value_catalog`.
4. `CREATE [UNIQUE] INDEX IF NOT EXISTS`: `ix_parameter_value_in_force (param_key, environment, valid_from)
   WHERE status = 'APPROVED'`; `ix_parameter_value_load (load_id)`; `ux_parameter_value_version_all
   (param_key, environment, COALESCE(product_group,'*'), version_no)` (the v6 unique key treats NULL product
   groups as distinct); `ux_parameter_value_approved_from (param_key, environment,
   COALESCE(product_group,'*'), valid_from) WHERE status IN ('APPROVED','IN_FORCE')`.
5. `COMMENT ON` tables and columns (as the pack, plus the three new columns).
6. Seed catalog: `INSERT ... ON CONFLICT (param_key) DO NOTHING`, the 19 rows of §12.4.
7. Seed values (SPEC-006): `INSERT ... SELECT ... WHERE NOT EXISTS` a row for (key, environment,
   product_group NULL).
8. Self-check `DO` block (SPEC-006), restricted to rows with `default_value IS NOT NULL`, so a required
   ENV-sourced key without a default (`temporal.target`) does not fail it.

The pack's `ix_parameter_value_lookup` (product-group lookup) is not carried: product values are
RWB-E1-045's. No GRANT: `recovery_svc` gets DML through the default privileges for `rwb_migrator` objects
(`infra/postgres/init/20-grants.sql.inc`).

### 12.4 Bootstrap catalog (19 rows; owners and "used by" are assumptions unless the source column says otherwise)

| key | kind | type | unit | min..max | default | scope | req | owner | value_source (property) | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| case.entry.dpd | BUSINESS | INTEGER | CALENDAR_DAYS | 1..365 | 90 | GLOBAL | yes | RW-COE | TABLE | story v7 Background (owner, range, default), DL16 |
| refdata.cache.ttl-seconds | ENVIRONMENT | INTEGER | SECONDS | — | 300 | GLOBAL | yes | RW-PLATADM | TABLE | story §3, DL11; AC4, AC8 |
| config.cache.ttl-seconds | ENVIRONMENT | INTEGER | SECONDS | — | 60 | GLOBAL | no | RW-PLATADM | TABLE | story §13, DL11 (assumed) |
| caselist.export.maxrows | BUSINESS | INTEGER | COUNT | — | 10000 | GLOBAL | no | RW-COE | TABLE | story §3, DL11 |
| ace.db.password | ENVIRONMENT | STRING | — | — | — | GLOBAL | no | RW-PLATADM | SECRET | AC9, DL26 |
| recon.caselist.tolerance.pct | BUSINESS | DECIMAL | PERCENT | — | 0.00 | GLOBAL | no | RW-COE | TABLE | pack [S-20], DL25 (assumed) |
| caselist.allocation.wait.until | BUSINESS | TIME | TIME_OF_DAY | — | 07:15 | GLOBAL | no | RW-COE | TABLE | pack [S-20] |
| servicelevel.required-statuses | BUSINESS | CODE_LIST | — | — | NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL | GLOBAL | yes | RW-COE | TABLE | pack [S-20], DL22 (assumed) |
| ENTRY_DPD | BUSINESS | INTEGER | DAYS | — | — | PRODUCT | yes | RW-PRODHEAD | TABLE | RWB-E1-045 BR2 [S-11 line 143] |
| EXCLUSION_LIST | BUSINESS | CODE_LIST | — | — | — | PRODUCT | yes | RW-PRODHEAD | TABLE | RWB-E1-045 BR2 |
| NOTICE_PERIOD_DAYS | BUSINESS | INTEGER | DAYS | 1..365 | — | PRODUCT | yes | RW-PRODHEAD | TABLE | RWB-E1-045 BR2; range from pack |
| CURE_PERIOD_DAYS | BUSINESS | INTEGER | DAYS | — | — | PRODUCT | yes | RW-PRODHEAD | TABLE | RWB-E1-045 BR2 |
| EXPOSURE_BAND_SET | BUSINESS | CODE_LIST | — | — | — | PRODUCT | yes | RW-PRODHEAD | TABLE | RWB-E1-045 BR2 |
| temporal.target | ENVIRONMENT | STRING | — | — | — | GLOBAL | yes | RW-PLATADM | ENV (`rwb.temporal.target`) | D-RCV-36 §3.1 (key) |
| temporal.namespace | ENVIRONMENT | STRING | — | — | rwb-recovery | GLOBAL | no | RW-PLATADM | ENV (`rwb.temporal.namespace`) | D-RCV-36 §3.1 (key; "Namespace" row) |
| temporal.taskqueue.platform | ENVIRONMENT | STRING | — | — | rwb-platform | GLOBAL | no | RW-PLATADM | TABLE | D-RCV-36 §3.1 (key; "Task queues" row) |
| temporal.retention.days | ENVIRONMENT | INTEGER | DAYS | — | 30 | GLOBAL | no | RW-PLATADM | TABLE | D-RCV-36 §3.1 (30, assumed, DL26) |
| drools.kiebase.cache.max | ENVIRONMENT | INTEGER | COUNT | — | 20 | GLOBAL | no | RW-PLATADM | ENV (`rwb.drools.kiebase-cache-max`) | D-RCV-36 §3.1 (20) |
| rules.testcases.min | BUSINESS | INTEGER | COUNT | — | 50 | GLOBAL | no | RW-COE | TABLE | D-RCV-36 §3.1 (50); pack Appendix A |

All rows list environments `DEV,SIT,UAT,PROD`; `secret=false` except `ace.db.password`. Ranges marked "—"
have no source and stay empty (A-08). "Used by": the pack's values for the first 13 rows;
`recovery.workflow (RWB-E1-070, RWB-E1-071)` for the four `temporal.*` keys, plus `RWB-E2-039` for
retention; `recovery.rules (RWB-E1-072)` for `drools.kiebase.cache.max`; `RWB-E1-073` for
`rules.testcases.min` (A-07). Seeded value rows: 10 TABLE GLOBAL non-secret rows with a default x 4
environments = 40 rows.

### 12.5 Load checks (SPEC-012), in this order; the first failure refuses the whole load

| # | Check | Refusal |
|---|---|---|
| 1 | file content and `validFrom` present | 422 MSG-GEN-001 `{field}` |
| 2 | UTF-8 CSV with header `key,environment,value` and at least one row | 422 MSG-GEN-001 `{field}=file` / MSG-P1-002 `{check}` |
| 3 | `validFrom` not before `BusinessDateProvider.today()` | 422 MSG-P3-027 `{check}="valid from is before the business date"` |
| 4 | per row, in file order: key in the catalog | 422 MSG-P1-002 `{check}="key <k> is not in the catalog"` |
| 5 | key loadable: not secret, not PRODUCT scope, not ENV-sourced | 422 MSG-P1-002 `{check}="key <k> cannot be loaded as a value"` |
| 6 | environment listed in the key's `environments` | 422 MSG-P1-002 `{check}="environment <e> is not listed for <k>"` |
| 7 | value not blank | 422 MSG-GEN-001 `{field}="value of <k>"` |
| 8 | value parses as the type | 422 MSG-P1-002 `{check}="value is not <TYPE>"` (AC6) |
| 9 | value within min..max | 422 MSG-GEN-002 `{field}=<k>`, `{min}`, `{max}` (AC5) |
| 10 | no duplicate (key, environment) in the file | 422 MSG-P1-002 `{check}="duplicate row for <k> <e>"` |
| 11 | identical repeat (SPEC-013) | existing load, `repeat = true` |
| 12 | no APPROVED row of (key, environment) with `valid_from >= validFrom` | 409 MSG-P3-027 `{check}="an approved version from <date> exists for <k> <e>"` |

### 12.6 Canonical form and content hash (SPEC-013)

Each value is stored as loaded, trimmed. The hash input is the rows sorted by key, then environment, each
line `key|environment|value`, joined with `\n`, UTF-8; SHA-256, lower-case hex.

### 12.7 Validity recomputation (SPEC-014, SPEC-015)

After every approval or rollback, for each affected (key, environment, product_group NULL): order the
APPROVED rows by `valid_from`; each row's `valid_to` is the next row's `valid_from` minus one day; the last
row's `valid_to` is NULL. Rows in other statuses keep `valid_to` NULL. Approval and rollback run in one
transaction with the load's rows locked (`SELECT ... FOR UPDATE`); the `version` column guards stale writes
(MSG-GEN-004).

### 12.8 Cache and refresh (SPEC-009, SPEC-018)

Per instance, keyed by (key, environment): the list of APPROVED versions. Built lazily; expires after
`config.cache.ttl-seconds` (the generated default 60 while the cache loads itself). On
`ParameterVersionApproved` (`@TransactionalEventListener(AFTER_COMMIT)`) and after a local rollback the
affected entries are rebuilt. Other instances see a change within the TTL until RWB-TE-006 adds the outbox.
The cache never holds VALIDATED or ROLLED_BACK rows, and never secrets.

### 12.9 Readiness (SPEC-016)

Health indicator `parameterCatalog`, added to the readiness group
(`management.endpoint.health.group.readiness.include: readinessState,parameterCatalog`). Evaluated at start-up
and on each probe from a result refreshed with the cache. DOWN details (shown to RW-PLATADM only, per the
existing `show-details: when-authorized`): `messageCode` MSG-P3-032 and a list of `{name, environment}`. One
WARN log line per missing key with the EN text. The process keeps running so readiness can recover after a
load (CLAR-012). With the flag off, only defaults and ENV properties are checked.

### 12.10 Access (SPEC-020)

`GET /admin/parameters` carries
`@PreAuthorize("@capabilityCheck.require(authentication, 'Rules and parameters', 'R', 'read parameters')")`.
Interim grants file `backend/src/main/resources/platform/interim-capability-grants.csv` (`role,area,rights`)
holds the "Rules and parameters" column of Users, Roles and Permissions v4 for every RW- role [S-07 lines
76-110], for example RW-COE CRUD, RW-RISK RA, RW-REFADM R, RW-PLATADM R, RW-TRIBE R, RW-AUDIT R,
RW-PHONECOL none. RWB-E1-037 replaces the implementation and deletes the file. The Reference data rights
(C, A, U) are checked on RWB-E1-043's endpoint; Reference data A is held by no role in S-07, and the
assumed grants (RW-RISK, DL01; the parameter owner, story §3) are recorded for RWB-E1-043 and RWB-E1-037
(CLAR-013).

### 12.11 Build checks (SPEC-003, SPEC-004, SPEC-005)

- Both checks are JUnit tests in `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/`, in the
  pattern of `RecoveryMigrationLintTest`, so `./gradlew check` fails on a finding. No new dependency
  (AGENTS §4.4): a small tokenizer in test code strips comments and reads literals.
- Fixture modules for AC2, AC3 and the PRODUCT exemption live under
  `backend/src/test/resources/architecture/fixtures/` (for example `recovery/casewf/casecreation/EntryRule.java`
  with a literal 90; a reader of `ParameterKey.of("allocation.retry.limit", Integer.class)`; a catalog with a
  PRODUCT row and no default). They are not compiled.
- Magic-number baseline `backend/src/test/resources/architecture/magic-number-baseline.csv`
  (`path,literal,count,reason,owner`), starting with the literals in today's code: `ApiError` HTTP status
  codes 401, 403, 404, 503 (protocol, not business); `DroolsRuleEngine` 16 and 0.75f (map sizing);
  `PdpaPayloadCodec` 12, 128, 16, 24, 32 (AES-GCM sizes); `PlatformSmokeWorkflow` 5 and 3 (smoke timeout and
  attempts, owner RWB-E1-071); `WorkflowIds` "rwb-recovery" and "rwb-platform" (equal to the defaults of
  `temporal.namespace` and `temporal.taskqueue.platform`, owner RWB-E1-071). The plan re-derives the exact
  list from the code. A stale or miscounted entry fails.
- `ParameterKeys` generation: a Gradle task in `backend/build.gradle.kts` reads the catalog file and writes
  `build/generated/sources/parameterKeys/.../platform/api/ParameterKeys.java`; `compileJava` depends on it.
  The catalog sits under `backend/src/main/resources/config/` because the Docker build context is `./backend`
  and copies only `src` (`backend/Dockerfile`; `docker-compose.yml` line 120).

### 12.12 Feature flag (SPEC-021)

`rwb.p3.configservice: ${RWB_P3_CONFIGSERVICE:false}` in `application.yaml`;
`${RWB_P3_CONFIGSERVICE:true}` in `application-local.yaml`. Added to `RecoveryProperties.P3` and
`RecoveryFlags`; `RecoveryFlags` keeps a two-argument constructor (configservice false) so
`DroolsRuleEngineTest` in the rules module is unchanged.

### 12.13 Logging

Structured logs only; no secret values; no user IDs in the interim decision line (loadId, table, keys,
validFrom, decision code). Load refusals log the message ID and check, never the file.

## 13. Frontend Specification

NOT_APPLICABLE. No screen in this story (story v7 §15); SCR-39 is Epic 8. `GET /admin/parameters` is
backend-only in this story. `frontend/src/api/schema.d.ts` is not regenerated (no OpenAPI change). The extra
`flags.configservice` field in `/platform/info` needs no frontend change.

## 14. Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | §13 | Story v7 §15; no OpenAPI change; no screen or client call | n/a |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions (methods) on the changed recovery packages, measured by `recoveryCoverageVerification` (JaCoCo); the plan adds it to `check` (plan input 12) | SPEC-001 to SPEC-027 | New service, interface, controller, checks, migration | Positive: every AC path. Negative: every row of §12.5, approval by the author, rollback with no earlier version, empty reason, secret read. Boundary: 1 and 365 accepted, 0 and 366 refused; `validFrom` equal to the business date accepted, one day before refused; reads on `valid_from - 1` and on `valid_from`. Error path: database unavailable on GET 503; concurrent approval 409 |

No measured coverage is claimed here.

## 15. Test scenarios

Levels in this repository: Unit and build checks (`test`); System (`recoveryIntegrationTest`, tag
`recovery-it`: Spring Boot context, Testcontainers PostgreSQL 16 built as the local stack; the
`ParameterLoadHandler` bean is called directly, because no endpoint exposes it until RWB-E1-043; GET through
MockMvc with Spring Security test JWTs carrying synthetic `sub` UUIDs and roles). "U-41" is a synthetic label
for a fixed synthetic UUID. RWB-E1-043 adds the HTTP-level tests of the three load operations.

| TC | Covers | Level | Data | Expected | Status |
|---|---|---|---|---|---|
| TC-E1-042-01 | AC1, BR1 | System | seed; PROD context; date 2026-12-01 | 90, versionNo 1 | Ready |
| TC-E1-042-02 | AC2, BR1, X1 | System (build check on fixture module) | fixture `recovery/casewf/casecreation` with literal 90 | check fails naming file, line, `case.entry.dpd` | Ready |
| TC-E1-042-03 | AC3, BR2, X2 | System (build check on fixture module) | fixture reading `allocation.retry.limit` | fails naming `allocation.retry.limit`; the real catalog has zero findings | Ready |
| TC-E1-042-04 | AC4, BR7, X3 | System | UAT context; `refdata.cache.ttl-seconds` UAT rows deleted and default cleared in the test DB | readiness DOWN, MSG-P3-032 with key and UAT | Ready |
| TC-E1-042-05 | AC5, X4 | System (interface) | load `case.entry.dpd,PROD,400` | 422 MSG-GEN-002 min 1 max 365; nothing written | Ready |
| TC-E1-042-06 | AC6, X5 | System (interface) | `case.entry.dpd,PROD,ninety` | 422 MSG-P1-002 "value is not INTEGER" | Ready |
| TC-E1-042-07 | AC7, BR4, X6 | System (interface) | versions 1-2 approved; U-41 loads v3 and approves it | 409 MSG-P7-002; status VALIDATED | Ready |
| TC-E1-042-08 | AC8 | System | 30 approved for SIT; PROD 300; contexts with `rwb.environment` SIT and PROD | 30 and 300 | Ready |
| TC-E1-042-09 | AC9, BR6, X7 | System | GET as RW-COE | `ace.db.password` with owner, environments, usedBy; no value fields | Ready |
| TC-E1-042-10 | AC10, X8 | System (interface) | v2 approved over v1; rollback with reason | v1 in force, 90; v2 ROLLED_BACK | Ready |
| TC-E1-042-11 | AC11, BR5, X10 | System (interface) | business date 2026-12-05; v2 = 91 PROD from 2026-12-10 loaded by one synthetic user, approved by another | 90 on 12-09, 91 on 12-10, same context | Ready |
| TC-E1-042-12 | X9 (access) | Access | RW-PHONECOL session from RWB-E1-022; matrix PM-2026.11 from RWB-E1-037 | 403 problem+json MSG-P4-002, action "read parameters", no array, one refusal event | **Blocked** (OI-E1-042-001). Exit: after RWB-E1-037 loads PM-2026.11 and RWB-E1-022 resolves the RW-PHONECOL test identity, run it; Pass only on that evidence |
| TC-E1-042-13 | SPEC-001/002/006 | System | empty schema | migration applies; tables, constraints, indexes; 19 + 40 seed rows | Ready |
| TC-E1-042-14 | SPEC-001/002 | System | schema built from Physical Schema v6 (local init) | migration applies; columns and constraints added; no error | Ready |
| TC-E1-042-15 | SPEC-001 | Unit | existing `RecoveryMigrationLintTest` | passes with the new file | Ready |
| TC-E1-042-16 | SPEC-013 | System (interface) | same content and validFrom twice | same loadId, `repeat = true`, one set of rows | Ready |
| TC-E1-042-17 | SPEC-013 | System (interface) | different value, same key/env/validFrom as an approved load | 409 MSG-P3-027 | Ready |
| TC-E1-042-18 | SPEC-015 | System (interface) | rollback with blank reason | 422 MSG-GEN-001 field reason | Ready |
| TC-E1-042-19 | SPEC-015 | System (interface) | a key whose only approved version comes from one load; roll that load back | 409 MSG-P3-015 | Ready |
| TC-E1-042-20 | SPEC-014 | System (interface) | two concurrent approvals | one APPROVED, one 409 MSG-GEN-004 | Ready |
| TC-E1-042-21 | SPEC-003 | Unit | fixture catalog with a PRODUCT row and no default | no finding; the same row without owner fails | Ready |
| TC-E1-042-22 | SPEC-021 | System | flag off | GET 404; no `ParameterLoadHandler` bean; `get` returns the default, versionNo 0 | Ready |
| TC-E1-042-23 | SPEC-012/023 | System (interface) | unknown key; empty file; validFrom before the business date | 422 MSG-P1-002; MSG-GEN-001; MSG-P3-027 | Ready |
| TC-E1-042-24 | SPEC-020 seam | System | GET with a test JWT for a role without Rules and parameters R | 403 MSG-P4-002 "read parameters". Does not close TC-12 | Ready |
| TC-E1-042-25 | SPEC-004 | Unit | baseline with a stale entry; code with an unlisted literal | both fail | Ready |
| TC-E1-042-26 | SPEC-005/024 | Unit | generated keys; `rwb.drools.kiebase-cache-max=20` | typed constants; ENV key served from the property | Ready |
| TC-E1-042-27 | SPEC-002/006/024 | System | after Flyway | DB catalog equals the CSV (19 rows); value seed equals the defaults | Ready |
| TC-E1-042-28 | SPEC-009/018 | System (interface) | approval | one event after commit with the §11.4 fields; cache rebuilt; no event on refusal | Ready |
| TC-E1-042-29 | SPEC-019/027 | System (interface) | approval | recorder called once with AC-VERS; log line has no user ID | Ready |
| TC-E1-042-30 | SPEC-022/025 | Unit | each §10.3 ID | EN and TH present with the same placeholders; Problem fields set | Ready |
| TC-E1-042-31 | SPEC-011 | System | filters key prefix, kind, owner, environment | filtered lists; PRODUCT rows without value | Ready |

## 16. Authority

| Who | What they may do (source) | Enforced where |
|---|---|---|
| RW-COE | Owns the catalog; loads (Reference data C), rolls back (U), reads; approves as parameter owner (assumed A) [S-01 §3, §10; S-07 line 101] | Read: this story. Load, approve, rollback rights: RWB-E1-043's endpoint |
| RW-REFADM | Loads (Reference data C), rolls back (U), reads (Rules and parameters R) [S-01 §3; S-07 line 107] | as above |
| RW-RISK | Approves where a threshold or limit moves (Reference data A, assumed grant, DL01) [S-01 §3, §10]; holds Rules and parameters RA and Reference data R in S-07 line 100 | as above (CLAR-013) |
| Parameter owner (catalog `owner_role`) | Approver per story §3 | RWB-E1-043 / RWB-E1-037 (CLAR-013) |
| Any approver | Must not be the author (BR4) | This story (`ParameterLoadHandler`, DB check) |
| RW-PLATADM | Owns environment settings; reads (Rules and parameters R) [S-01 §10; S-07 line 106] | This story |
| RW-TRIBE | Adds catalog entries through reviewed PRs; reads [S-01 §10] | Merge review; this story |
| Any role with Rules and parameters R | Reads the catalog | This story |
| RW-PHONECOL | No Rules and parameters right; refused [S-07 line 76] | This story (TC-12 blocked) |
| Delegation of authority | Not applicable: a parameter is not a credit decision [S-01 §10] | — |

## 17. Guardrails and controls

- No business value in code (SPEC-004); no new dependency; no personal data; synthetic UUIDs only.
- Secrets: listed, never stored or served (SPEC-010, DB check).
- Maker-checker in the interface and the database (SPEC-014).
- Audit: author, approver, times and rollback reason in `parameter_value`; AC-VERS through the recorder seam
  (SPEC-019). The access log is RWB-E1-039 (phase0 A-18).
- D-RCV-35: Workbench-owned reference data in `recovery`; no `public` read; no source load.
- D-RCV-36: the six keys are catalog rows; no Temporal or Drools call in this story.

## 18. Out of scope

- The shared reference-load endpoint and its dispatch, the other table codes, and `/verify` (RWB-E1-043,
  D-RUN-10, D-RUN-11).
- Product-specific parameter values and service levels (RWB-E1-045).
- Dated feature flags and the flag table (FEAT-CWC-26, RWB-E1-047).
- The parameter administration screen (Epic 8, FEAT-ADM-01).
- The change checklist and audit report, including `changeRequestRef`, `impactSummary` and `rollbackPlan`
  (RWB-E2-041) [S-01 §19].
- Decision log store and writer (RWB-E1-008, RWB-E1-027); outbox (RWB-TE-006); permission matrix and sessions
  (RWB-E1-037, RWB-E1-022); moving the Temporal and Drools reads to `ParameterService` (RWB-E1-071,
  RWB-E1-072); the message table (unowned).

## 19. Clarification Log

No question is asked in this run (RUN-BRIEF rule 4, L-RCV-03, AGENTS §10.6). Each item carries a labelled
default (`assumptions.md`) and, where it is an open item, a row in `shared-updates.md`. The pack's items stay
open; where the evidence settles an item for this spec, the row says so, but closing the register entry is
the owner's decision (triage decision (e)).

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | OI-E1-042-001; X9; TC-12 | The access test needs RWB-E1-022 sessions and the RWB-E1-037 matrix | TC-12 cannot run in this window | Not asked. Default: Blocked with exit criterion | OPEN (non-blocking) | 011, 020 |
| CLAR-002 | OI-E1-042-002; D-RCV-28 | The two-file names fail the lint | Migration design | Not asked. Settled for this spec by D-RCV-28 and D-RUN-07: one file, number at merge | OPEN in register; settled for this spec | 001 |
| CLAR-003 | OI-E1-042-003; PRE-2 | Full Epic 1 catalog file absent | Later stories add their keys | Not asked. Default: 19-row bootstrap (§12.4); each later story adds its rows by PR and migration | OPEN (non-blocking) | 003, 006 |
| CLAR-004 | OI-E1-042-004; AGENTS §3.6 | No message table | Message source | Not asked. Default: fixed catalog behind `MessageResolver` | OPEN (non-blocking) | 022 |
| CLAR-005 | OI-E1-042-005 | No per-code CSV template register | Only the PARAMETER template is defined here | Not asked. Default: PARAMETER header `key,environment,value` (pack §3.3) | OPEN (non-blocking; RWB-E1-043) | 012 |
| CLAR-006 | OI-E1-042-006; finding 117 | Naming conflicts (`case.entry.dpd` / `case.entry.dpd_threshold` / `ENTRY_DPD`; prescription and tolerance keys) | Two keys for one concept | Not asked. Default: `case.entry.dpd` is the GLOBAL key; `ENTRY_DPD` is RWB-E1-045's product key; the other names are not seeded | OPEN (decision needed) | 006 |
| CLAR-007 | OI-E1-042-007; AC3 | PRODUCT rows have no default | Completeness rule | Not asked. Default: exempt PRODUCT from the default rule (pack recommendation) | OPEN in register; applied | 003 |
| CLAR-008 | OI-E1-042-008; finding 104 | No load-to-rows link | Approve and rollback by loadId | Not asked. Default: pack option A, `load_id` plus `content_hash` and `rollback_reason`; Physical Schema update requested | OPEN (schema owner) | 002, 014, 015 |
| CLAR-009 | OI-E1-042-009 | `recoverySchema` placeholder property | Migration placeholder | Not asked. Settled for this repository by `RecoveryFlywayConfig.java:37` (`placeholders(Map.of("recoverySchema", schema))`); the pack's property is not needed here | OPEN in register; settled for this spec | 001 |
| CLAR-010 | OI-E1-042-010 | PRODUCT targets, DOCUMENT_HUB_PARAMETER, RETENTION_CLASS | Other table codes | Not asked. Outside this story; dispatch is RWB-E1-043's (D-RUN-10, D-RUN-11) | OPEN (RWB-E1-043 and owners) | 017 |
| CLAR-011 | OI-E1-042-011; finding 106 | OpenAPI lacks `required`, `format`, repeat status | Contract hardening | Not asked. Default: enforced in the interface; identical repeat answered 201 with the same body; conflict 409 | OPEN (API owner) | 012, 013 |
| CLAR-012 | X3 vs AC4 | X3 says "does not start"; AC4 says health fails and no traffic | Start-up behaviour | Not asked. Default: readiness DOWN, process up (AC4 is the testable statement) | OPEN (non-blocking) | 016 |
| CLAR-013 | BR4; story §3; S-07; API v4 line 3232 | Reference data A held by no role; owner-per-key and "Risk where a threshold moves" routing undefined | Who may approve | Not asked. Default for RWB-E1-043 and RWB-E1-037: Reference data A to RW-COE (owner) and RW-RISK (DL01); routing not encoded. This story enforces only author <> approver | OPEN (RWB-E1-043, RWB-E1-037, business) | 014 |
| CLAR-014 | Story §13 vs AC8 | §13: environment settings come from the environment; AC8 loads table values for an ENVIRONMENT-kind key | Value source | Not asked. Default: `value_source` column; TABLE unless the setting already comes from a Spring property or the secret store | OPEN (non-blocking) | 024, 012 |
| CLAR-015 | RWB-E1-043 §3 line 45 | Business date source (`v_ace_batch_status`) arrives later | Load check, GET | Not asked. Default: interim Asia/Bangkok date behind `BusinessDateProvider` | OPEN (non-blocking) | 023 |
| CLAR-016 | Story §12 event; finding 116 | One `versionNo` for a multi-key load; event not in the catalog | Payload | Not asked. Default: §11.4 payload | OPEN (event catalog owner) | 018 |
| CLAR-017 | Finding 110 | Seed provenance and in-force date | Seed rows | Not asked. Default: seed identity UUID, approver NULL, valid_from 2026-11-02, baseline approved by the reviewed catalog PR | OPEN (non-blocking) | 006 |
| CLAR-018 | D-RCV-36 §3.1; finding 108 | Six keys lack kind, type, owner, range, required flag | Catalog rows | Not asked. Default: §12.4, owners and used-by labelled assumptions | OPEN (non-blocking) | 024 |
| CLAR-019 | Pack §3.6 | 503 message ID undecided | Problem on outage | Not asked. Default: MSG-GEN-006 (pack candidate) | OPEN (message owner) | 025 |
| CLAR-020 | Story §13 package; plan input 5; phase0 A-01 | No `casewf` module; the module map is RWB-TE-001's | Package | Not asked. Default: `platform` module | OPEN (RWB-TE-001) | 026 |
| CLAR-021 | E6; S-08 | No message for an unknown reference load | 404 text | Not asked. Default: existing MSG-P4-003 | OPEN (non-blocking) | 017, 025 |
| CLAR-022 | RWB-E1-043 §3 line 41 | RWB-E1-043 expects this story to serve "the list of reference table codes"; story v7 RWB-E1-042 does not specify it | Interface | Not asked. Default: not served here; table codes and dispatch are RWB-E1-043's (D-RUN-10, D-RUN-11); this story exposes `ParameterLoadHandler.TABLE = "PARAMETER"` | OPEN (RWB-E1-043) | 017 |
| CLAR-023 | Approval after `validFrom` has passed; rollback of a non-approved load | Not in the sources | 409 rules | Not asked. Default: both refused with MSG-P3-027 (§8) | OPEN (non-blocking) | 014, 015 |

## 20. Design evidence and status

No Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5): N/A. No UI in scope. Contract
artefacts (`contracts/backend-apis.json`, `frontend-integrations.json`) are not written: the run's file list
is fixed to seven files, and the one exposed operation is in API v4 unchanged; §11 holds the contract.

```text
MCP_STATUS_SUMMARY: No MCP connected (RUN-BRIEF rule 5); no Figma link; not needed (no UI).
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New configuration service in the platform module; backend only; GET /admin/parameters implemented for the first time; loads served through a published interface that RWB-E1-043 exposes (D-RUN-10); no OpenAPI change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: no parameter code in this repository; GET exists in API v4 but not in code]
REQUIREMENT_COVERAGE_SUMMARY: All 7 BRs, 11 ACs, 10 exception paths, 10 flow steps, 5 preconditions, 3 transitions, authority, 5 contract items, messages and 4 guardrails mapped; TC-12 is blocked by later stories, not by a missing rule.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 57] [COVERED_RULES: 57] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
SPEC_CLARIFICATION_STATUS: OPEN_ITEMS_RECORDED [OPEN_ITEMS: 23] [BLOCKING: 0] [UNBLOCK_ACTION: orchestrator applies shared-updates.md; owners answer the open items; none blocks planning]
```

The two source contradictions (X3 vs AC4; story §13 vs AC8) and the ambiguities are settled by labelled
defaults (CLAR-012, CLAR-014 and the rest) and recorded as document gaps, so they are counted as covered,
not as open contradictions.
