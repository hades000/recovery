---
title: "Tasks — RWB-E1-043 Reference data service with versioned tables"
run_id: "INC-009-epic-1-RWB-E1-043"
story: "RWB-E1-043"
jira: "TB0001-1204"
---

# Tasks — RWB-E1-043

Design Source: NOT_REQUIRED (`UI In Scope: NO`).

Plan: `plan.md`. All paths in `ace-monorepo/` unless they start with `output/` or `docs/`. ACE branch `feature/TB0001-1204-reference-data-versions` from `develop`; commit message `TB0001-1204: <summary>`. Task IDs are written `TASK-RWB-E1-043-NN`; the short form `TASK-NN` in `plan.md` means the same task.

**Every build task is blocked by TASK-RWB-E1-043-00 (plan-approval preconditions).** PRE-1 through PRE-8 (Product Owner spec/backlog approval, FDA design confirmation, the REVIEW-RWB-E1-043-001 Low finding, RWB-E1-044/RWB-E1-042/RWB-E1-022 merge verification, plan approval, task approval) are **all pending** at plan time (`plan.md` §Plan approval preconditions). If PRE-4, PRE-5 or PRE-6 is still not true when Builder reaches TASK-01, Builder stops and reports `NEXT_STEP` rather than stubbing the missing interface.

## Unit test applicability

| Surface | Status | Trace | Reason | Unit-test tasks |
|---|---|---|---|---|
| Frontend | NOT_APPLICABLE | — | No screen, component, route or label change (`Frontend Changes Required: NO`) | — |
| Backend | REQUIRED | SPEC-RWB-E1-043-001..014; FR-RWB-012, FR-RWB-020 | New registry, read service, cache, schema checks, repositories, logger, controllers are executable code | TASK-RWB-E1-043-15, -16, -17, -18; gate TASK-RWB-E1-043-20 |

## Task table

### Gate and setup

| TASK ID | Description | Trace (SPEC/FR/NFR) | BLOCKED_BY | Verification |
|---|---|---|---|---|
| TASK-RWB-E1-043-00 | **Plan-approval precondition check.** Confirm in `docs/increments/INC-009-epic-1-RWB-E1-043.md` "Owners and approvals" and `docs/open-items.md` that PRE-1 (Product Owner spec/backlog approval, GAP-006), PRE-2 (FDA design/architecture confirmation, GAP-006), PRE-3 (REVIEW-RWB-E1-043-001 disposition — RW-RISK Reference-data-A grant loaded through RWB-E1-037 before SIT approval), PRE-7 (FDA plan approval) and PRE-8 (FDE task approval) each have a decision and a date. If any is missing, stop with `BLOCKED`. | GAP-006; D-RCV-15; REVIEW-RWB-E1-043-001 | NONE | Builder records the five decisions with dates in `output/INC-009-epic-1-RWB-E1-043/implement/report.md` |
| TASK-RWB-E1-043-01 | **Branch, merge-order and precondition verification.** Create `feature/TB0001-1204-reference-data-versions` from current `develop`; record the `develop` SHA. The `docs/increments/INDEX.md`-vs-`output/INC-001-epic-1-RWB-E1-044/specify/spec.md` status conflict (plan.md §Risks) is resolved: spec.md now reads `status: "SPECIFIED"`, and RWB-E1-044's plan and task gates were approved 2026-11-10 13:41 by Jesniphat Pukkham — this does not by itself prove the Flyway bean is merged to `develop`, so Builder still verifies directly against `develop`: (a) PRE-4 — the RWB-E1-044 Flyway bean (own bean, own history table `flyway_schema_history_recovery`, `baselineVersion("0")`, `baselineOnMigrate(true)`, `createSchemas(false)`, D-RCV-47/D-RCV-48 — no `${recoverySchema}` placeholder, tables live unqualified in schema `ace`) exists; (b) PRE-5 — RWB-E1-042's published `ConfigurationService` interface and `refdata.cache.ttl-seconds` exist; (c) PRE-6 — `RecoveryAccessGuard` and the role-to-session mapping from RWB-E1-022 exist. Query the LOV-REF-TABLE row count; if fewer than 13 rows, stop (do not seed business values). If any of (a)/(b)/(c) is absent, stop and report `NEXT_STEP`; do not stub the missing interface. | PRE-4, PRE-5, PRE-6 (plan.md); D-RCV-47, -48, -34, -36 | TASK-RWB-E1-043-00 | Facts (bean presence, interface presence, guard presence, LOV-REF-TABLE row count, `develop` SHA) recorded in `implement/report.md` |

### Backend Plan

| TASK ID | Description | Trace (SPEC/FR/NFR) | BLOCKED_BY | Verification |
|---|---|---|---|---|
| TASK-RWB-E1-043-02 | **Package skeleton.** Inside the existing `casewf` module (`backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/`, main-scope skeleton already created by RWB-TE-001 TASK-02), add `refdata/package-info.java` (no annotation — a feature folder, not a new `@ApplicationModule`), `refdata/api/package-info.java` with `@NamedInterface("api")`, `refdata/internal/package-info.java` with no annotation. No other new type in main scope at this task. | plan.md §Package and file layout; D-RCV-02, -36 | TASK-RWB-E1-043-01 | `find backend/src/main/java/.../recovery/casewf/refdata -name package-info.java` lists exactly 3 files; `./gradlew compileJava` |
| TASK-RWB-E1-043-03 | **Migration.** `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_043_reference_versions.sql` per `data-model.md` §1: `rwb_reference_version` and `rwb_reference_row` tables (unqualified, in schema `ace`, D-RCV-47/D-RCV-48), both unique constraints, the `ck_reference_version_approver_not_author` check, the `rwb_ux_reference_version_table_validfrom_approved` partial unique index, and the two append-only triggers, verbatim as drafted in `data-model.md`. `<seq>` is **not pre-allocated** (RWB-E1-043 is absent from `docs/architecture/migration-merge-order-map.md`'s build-order table): take the next free 4-digit sequence at merge time (D-RCV-34), never renumber after apply. Line 1 is `-- Story: RWB-E1-043`. Re-verify the trigger SQL (notably `RAISE EXCEPTION` inside `BEFORE DELETE` and the `IS DISTINCT FROM` column list) against a running Testcontainers Postgres instance; the plan's SQL is design-time, not execution-verified. No `${recoverySchema}` placeholder, no bare schema literal, no `SET search_path`; every table/index name carries the `rwb_` prefix (D-RCV-47). | SPEC-RWB-E1-043-001; D-RCV-47, -48, -34 | TASK-RWB-E1-043-01, TASK-RWB-E1-043-02 | Flyway applies clean on a fresh Testcontainers schema; `flyway_schema_history_recovery` shows the migration; lint (`grep -n "SET search_path\|\\${recoverySchema}" <file>` empty; every `CREATE TABLE`/`CREATE INDEX` name starts with `rwb_`) |
| TASK-RWB-E1-043-04 | **JPA entities** (`refdata/internal/`): `ReferenceVersionEntity`, `ReferenceRowEntity`, `ReferenceVersionStatus` enum (`VALIDATED`, `APPROVED`, `ROLLED_BACK`) per `data-model.md` §3. `row_data` mapped as `jsonb` (Hypersistence or native `@JdbcTypeCode(SqlTypes.JSON)`, Builder's choice within ACE's existing jsonb-mapping convention). | SPEC-RWB-E1-043-001, -004 | TASK-RWB-E1-043-03 | `./gradlew compileJava`; entity fields match `data-model.md` §3 1:1 |
| TASK-RWB-E1-043-05 | **Repositories** (`refdata/internal/`): `ReferenceVersionRepository`, `ReferenceRowRepository` (Spring Data JPA, package-private or module-internal visibility — never exposed through `refdata.api`). Query methods: highest `version_no` for a table code; the APPROVED version in force for `(table_code, business_date)`; existing version by `(table_code, valid_from, content_hash)` (idempotency lookup, CLAR-005); rows by `version_id`. | SPEC-RWB-E1-043-001, -004, -006, -007 | TASK-RWB-E1-043-04 | `./gradlew compileJava`; covered by TASK-RWB-E1-043-15/-16 behaviour |
| TASK-RWB-E1-043-06 | **`ReferenceTableSchemas`** (`refdata/internal/`): resolves the LOV-REF-TABLE 13 codes and, per table code, the column-schema catalog entries from RWB-E1-042 (`CLAR-003`; `kind` value Builder's implementation choice within the catalog-entry mechanism) for the row/key check. Refuses an unknown table code before any schema/key check runs (BR1). No table code, column name or business value as a Java constant or literal (guardrail) — all read through the catalog/LOV interfaces. | SPEC-RWB-E1-043-002; BR1; CLAR-002, -003 | TASK-RWB-E1-043-01, TASK-RWB-E1-043-02 | Behaviour by TASK-RWB-E1-043-15 (TC-E1-043-12); `grep` of the class for a hardcoded table-code/column literal is empty |
| TASK-RWB-E1-043-07 | **`ReferenceVersionRegistryImpl`: load.** Runs the seven load checks from spec §Load checks (table code valid; schema/key check per row naming row+column on failure, BR5/AC4/AC10; `valid_from` not before the business date, BR6/AC6; empty-file refusal naming `rows`, X7/AC10); computes the SHA-256 content hash over rows sorted by key; on an identical-hash repeat load for the same `(table_code, valid_from)`, returns the existing load unchanged (CLAR-005, X4, AC7); otherwise assigns the next `version_no`, writes one VALIDATED `reference_version` plus its `reference_row` rows in one transaction. | SPEC-RWB-E1-043-001, -003, -004; BR2, BR5, BR6; AC4, AC6, AC7, AC10; X2, X3, X4, X7 | TASK-RWB-E1-043-05, TASK-RWB-E1-043-06 | Behaviour by TASK-RWB-E1-043-15 |
| TASK-RWB-E1-043-08 | **`ReferenceVersionRegistryImpl`: approval.** Refuses approval when there is no approver or the approver equals `author_user_id` (X1, AC2, MSG-P7-002); uses optimistic locking (a version column or `WHERE status = 'VALIDATED'` conditional update) so of two simultaneous approvals exactly one succeeds and the other gets MSG-GEN-004 (X5, AC8); on success sets `status = APPROVED`, `approver_user_id`, `approved_at`, and clears/sets the previously-in-force version's `valid_to` to the day before this version's `valid_from`. One transaction per approval. | SPEC-RWB-E1-043-005, -010; BR4, BR8; AC2, AC5, AC8; X1, X5 | TASK-RWB-E1-043-05 | Behaviour by TASK-RWB-E1-043-16 |
| TASK-RWB-E1-043-09 | **`ReferenceVersionRegistryImpl`: rollback.** Same endpoint-reuse shape recorded with RWB-E1-019 (CLAR-008): sets the rolled-back version's `status = ROLLED_BACK`. Per **IMPL-NOTE-01** (plan.md §Plan-time verification, §Risks — a planner inference beyond CLAR-008's literal text and the status-transition matrix, not a settled spec fact): also clears the superseded version's `valid_to` back to open-ended so it resumes being in force. Flag this inference explicitly in the PR/MR description for FDA/Technical Specifier confirmation before merge. **Error rule (REVIEW-RWB-E1-043-PLAN-001, approved disposition Option A — Jira `TB0001-1204` comment `1783253`, 2026-11-10):** 404 MSG-P4-003 only when `loadId` resolves to no `rwb_reference_version` row at all; 422 MSG-P3-027 when a row resolves but its `status` is not APPROVED. | spec.md §Feature flag and rollback; CLAR-008; IMPL-NOTE-01; REVIEW-RWB-E1-043-PLAN-001 | TASK-RWB-E1-043-05 | Behaviour by TASK-RWB-E1-043-17 (TC-E1-043-13, TC-E1-043-13b); PR description names IMPL-NOTE-01 explicitly |
| TASK-RWB-E1-043-10 | **`ReferenceDataServiceImpl`: `rows(tableCode, businessDate)`.** Resolves the latest APPROVED version with `valid_from <= businessDate` (and, if present, `businessDate <= valid_to`) for the table; returns its rows. Throws `NoVersionInForceException` (naming the table code and business date) when none exists (X6, AC9, BR9); this is the trigger for "engine does not start" and the alert — the engine's own start-up wiring is out of scope (spec "Impacted Existing Nodes", plan.md §Integration and cross-layer). Also backs the `GET .../lists/{listCode}` read (version history plus the in-force version) for TASK-13's list controller. | SPEC-RWB-E1-043-006, -007, -009; BR3, BR9; AC1, AC5, AC9 | TASK-RWB-E1-043-05 | Behaviour by TASK-RWB-E1-043-16 |
| TASK-RWB-E1-043-11 | **`ReferenceRowCache`.** Keyed by `(table_code, business_date)`; TTL from RWB-E1-042's `refdata.cache.ttl-seconds` (300s assumed, DL11, PRE-5); never caches a non-APPROVED version (spec §Cache and logging). Backed by `ReferenceDataServiceImpl` on a miss or expiry. | SPEC-RWB-E1-043-006, -007; data-model.md §4 | TASK-RWB-E1-043-10 | Behaviour by TASK-RWB-E1-043-18 (TC-E1-043-14) |
| TASK-RWB-E1-043-12 | **`ReferenceVersionLogger`.** One log line per table code per engine-start cycle or cache refresh (not per row, CLAR-007); the line carries table code, version number and business date only — no row-level content, no party/customer identifier (BR7, AC3, Security/privacy guardrail). | SPEC-RWB-E1-043-008; BR7; AC3; CLAR-007 | TASK-RWB-E1-043-10 | Behaviour by TASK-RWB-E1-043-17 (TC-E1-043-03) |
| TASK-RWB-E1-043-13 | **Controllers.** `ReferenceLoadController` (`refdata/internal/`, or module-internal web layer per ACE convention): `POST /api/recovery/v1/admin/reference-loads` (Reference data C — RW-REFADM, RW-COE for owned tables), `POST .../{loadId}/approve` (Reference data A — RW-RISK, assumed per DL01/CLAR-001), `POST .../{loadId}/rollback` (same right as approve, inferred — IMPL-NOTE-01). `ReferenceListController`: `GET /api/recovery/v1/admin/lists/{listCode}` (Reference data R — SY-CASEWF, SY-RULES, RW-AUDIT). Enforcement uses the RWB-E1-022 session/role mechanism (`RecoveryAccessGuard`, PRE-6); HTTP/MSG mapping exactly per spec §API change assessment and `contracts/backend-apis.json`: 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003, 409 MSG-P3-027/MSG-P7-002/MSG-GEN-004, 422 MSG-P3-027/MSG-GEN-001, 503. Plain JSON, uuid ids, no HAL (ADR-RCV-001). | SPEC-RWB-E1-043-005, -006, -009, -010; spec.md §Feature flag and rollback (rollback endpoint); plan.md §Authorization; ADR-RCV-001 | TASK-RWB-E1-043-07, TASK-RWB-E1-043-08, TASK-RWB-E1-043-09, TASK-RWB-E1-043-10 | Behaviour by TASK-RWB-E1-043-15, -16, -17 (integration half); `contracts/backend-apis.json` endpoint shapes match the controller response bodies |
| TASK-RWB-E1-043-14 | **Module-boundary verification.** Run the existing `RecoveryBoundaryTest` (RWB-TE-001 TASK-10) and `ModulithTest` against the new classes; `recovery-modules.yaml`'s `{code: P3, name: casewf, published: [api]}` entry already covers `casewf.api` (plan.md §Plan-time verification) — no edit to the module map. If a new class breaks a boundary rule, fix the class's package or visibility; never weaken the rule or the map. | SPEC-RWB-E1-043 (package/boundary guardrail); D-RCV-02, -36, -41 | TASK-RWB-E1-043-13 | `./gradlew test --tests "th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryTest"` and `--tests th.co.scb.ace.demo.ModulithTest` green |
| TASK-RWB-E1-043-15 | **Backend unit tests: load checks.** `ReferenceTableSchemasTest` (TC-E1-043-12) and `ReferenceVersionRegistryImplTest` load-side cases (TC-E1-043-04, -06, -07, -10), plus `ReferenceLoadControllerIT` (`@Tag("recovery-it")`) for the HTTP-reachable halves of the same scenarios. Synthetic fixture data only (SERVICE_LEVEL/LEGAL_PERIOD/REGION/DOCUMENT_TYPE rows invented for the test, no production content). | SPEC-RWB-E1-043-002, -003, -004; BR1, BR5, BR6; AC4, AC6, AC7, AC10; X2, X3, X4, X7 | TASK-RWB-E1-043-06, TASK-RWB-E1-043-07, TASK-RWB-E1-043-13 | `./gradlew test --tests "th.co.scb.ace.demo.recovery.casewf.refdata.*"` green; `./gradlew recoveryIntegrationTest` green |
| TASK-RWB-E1-043-16 | **Backend unit tests: approval and version resolution.** `ReferenceVersionRegistryImplTest` approval cases (TC-E1-043-02, -08) and `ReferenceDataServiceImplTest` (TC-E1-043-01b, -05b, -09), plus `ReferenceLoadControllerIT`/`ReferenceListControllerIT` (`@Tag("recovery-it")`) for the HTTP-reachable halves (TC-E1-043-01a, -02, -05a, -08). | SPEC-RWB-E1-043-005, -006, -007, -009, -010; BR3, BR4, BR8, BR9; AC1, AC2, AC5, AC8, AC9; X1, X5, X6 | TASK-RWB-E1-043-08, TASK-RWB-E1-043-10, TASK-RWB-E1-043-13 | `./gradlew test --tests "th.co.scb.ace.demo.recovery.casewf.refdata.*"` green; `./gradlew recoveryIntegrationTest` green |
| TASK-RWB-E1-043-17 | **Backend unit/integration tests: rollback and logging.** `ReferenceVersionRegistryImplTest` rollback case and `ReferenceLoadControllerIT` (`@Tag("recovery-it")`) (TC-E1-043-13, planner-added, IMPL-NOTE-01 explicitly named in the test's display name); `ReferenceVersionLoggerTest` (TC-E1-043-03). | SPEC-RWB-E1-043-008; spec.md §Feature flag and rollback; BR7; AC3; IMPL-NOTE-01 | TASK-RWB-E1-043-09, TASK-RWB-E1-043-12, TASK-RWB-E1-043-13 | `./gradlew test` and `./gradlew recoveryIntegrationTest` green; TC-E1-043-13's test name/comment cites IMPL-NOTE-01 |
| TASK-RWB-E1-043-18 | **Backend unit tests: cache TTL.** `ReferenceRowCacheTest` (TC-E1-043-14, planner-added): expired entry is not served and triggers a reload; a non-APPROVED version is never cached. | data-model.md §4; `refdata.cache.ttl-seconds` | TASK-RWB-E1-043-11 | `./gradlew test --tests "th.co.scb.ace.demo.recovery.casewf.refdata.internal.ReferenceRowCacheTest"` green |
| TASK-RWB-E1-043-19 | **Feature-flag catalog entry confirmation.** Verify `rwb.p3.refdata-versions` exists as a catalog/config entry (RWB-E1-042 mechanism, PRE-5) and defaults to a state where engines read the values loaded before this story when off (spec §Feature flag and rollback). No engine-side wiring in this task — the allocation/timer engines' own consumption of this flag are impacted existing nodes, out of scope (plan.md §Out of scope). | spec.md §Feature flag and rollback | TASK-RWB-E1-043-01 | Flag entry present; recorded in `implement/report.md` |

### Cross-cutting, compliance and release

| TASK ID | Description | Trace (SPEC/FR/NFR) | BLOCKED_BY | Verification |
|---|---|---|---|---|
| TASK-RWB-E1-043-20 | **Coverage gate, diff and guardrail check.** Run `./gradlew test recoveryIntegrationTest` then `./gradlew recoveryCoverageReport recoveryCoverageVerification` (JaCoCo, recovery-only class directories including `casewf/refdata/**`, RWB-TE-001 TASK-11); 80% LINE/INSTRUCTION/BRANCH/METHOD. `git diff --name-only develop...HEAD` limited to `casewf/refdata/**`, the one new migration file, and this story's test classes/fixtures — no edit to `ModulithTest.java`, `application.yaml`, security config, `recovery-modules.yaml`, other recovery modules, `.gitlab-ci.yml`, Jenkins files. No table code, column name, band, period or limit as a Java literal (guardrail). PII/secret scan of the diff. Save test results, JaCoCo XML/HTML and console output to `output/INC-009-epic-1-RWB-E1-043/implement/backend/`. | SPEC-RWB-E1-043-001..014; TS-RCV-4, -8; D-RCV-28 (3), -40 | TASK-RWB-E1-043-14, TASK-RWB-E1-043-15, TASK-RWB-E1-043-16, TASK-RWB-E1-043-17, TASK-RWB-E1-043-18, TASK-RWB-E1-043-19 | Exit codes 0; JaCoCo metrics ≥80% read from the XML; diff scope matches; evidence files present |
| TASK-RWB-E1-043-21 | **Release readiness, traceability and risk escalation.** Record ACE branch, commit SHAs and MR link in `output/INC-009-epic-1-RWB-E1-043/implement/`. Escalate to Context Updater/human: (a) confirm the RWB-E1-044 Flyway bean is actually merged to `develop` (the `INDEX.md`-vs-`spec.md` status conflict itself is resolved — spec.md `status: "SPECIFIED"`, plan/task gates approved 2026-11-10 13:41 — but that is a document-status fact, not a merge fact; plan.md §Risks); (b) the undeclared RWB-E1-022 dependency, with a request to add it to the increment card; (c) REVIEW-RWB-E1-043-001's Low finding disposition status for the SIT-approval gate (PRE-3). Update `requirement/Traceability_Matrix.md` CODE refs for SPEC-RWB-E1-043-001..014. Unit Test Evidence table per `.github/rules/implementation-execution-gates.md` (Backend row only; Frontend `NOT_APPLICABLE`). Commit/push/MR only when the user asks (CLAUDE.md two-repository rule). | SPEC-RWB-E1-043-001..014 (trace); plan.md §Risks; CLAUDE.md two-repository rule | TASK-RWB-E1-043-20 | Files present; matrix rows carry TASK and CODE refs; the three escalation items are recorded as open items with an owner |

## Dependency graph (DAG)

```text
00 ─► 01 ─┬─► 02 ─┬─► 03 ─► 04 ─► 05 ─┬─► 07 ─┬─► 13 ─┬─► 14 ─────────────┐
          │       │                 ├─► 08 ─┤       ├─► 15 ─┐            │
          │       │                 └─► 09 ─┘       ├─► 16 ─┤            │
          │       └─► 06 ───────────────────────────┤       ├─► 20 ─► 21
          ├─► 10 ─┬─► 11 ─────────────────────┬──────┤       │
          │       └─► 12 ─────────────────────┘       ├─► 17 ─┤
          └─► 19 ──────────────────────────────────────┴─► 18 ┘
```

No cycle. TASK-06 (schemas) and TASK-10/-11/-12 (read/cache/logger) can run in parallel with TASK-03..-05/-07..-09 (migration/entities/registry) once TASK-01/-02 complete; TASK-13 (controllers) needs the registry (07/08/09) and the read service (10); TASK-19 (feature flag) only needs TASK-01.

## Requirement and spec coverage

| SPEC | Tasks |
|---|---|
| SPEC-RWB-E1-043-001 | 03, 04, 05, 07, 15 |
| SPEC-RWB-E1-043-002 | 06, 15 |
| SPEC-RWB-E1-043-003 | 06, 07, 15 |
| SPEC-RWB-E1-043-004 | 03, 04, 05, 07, 15 |
| SPEC-RWB-E1-043-005 | 08, 13, 16 |
| SPEC-RWB-E1-043-006 | 05, 10, 11, 13, 16 |
| SPEC-RWB-E1-043-007 | 05, 10, 11, 16 |
| SPEC-RWB-E1-043-008 | 12, 17 |
| SPEC-RWB-E1-043-009 | 10, 13, 16 |
| SPEC-RWB-E1-043-010 | 08, 13, 16 |

SPEC-RWB-E1-043-011, -012, -013, -014 are not individually mapped above: spec.md's own "Requirement-to-SPEC Logic Coverage" table does not tie any of them to a BR/AC/X row — only the Unit Test Applicability table's range notation "SPEC-RWB-E1-043-001..014" implies their existence (plan.md §Requirement Logic To Task Coverage note). Per CLAUDE.md this plan does not invent what they individually cover; the rollback task (TASK-09, -13, -17) is instead traced to its real source — spec.md §Feature flag and rollback, CLAR-008, and the planner's own IMPL-NOTE-01 (FR/NFR table below) — rather than to a fabricated SPEC-014 claim.

| FR / NFR / requirement | Tasks |
|---|---|
| FR-RWB-012 (reference versioning and approval) | 03, 04, 05, 07, 08, 09, 10 |
| FR-RWB-020 (module-boundary / published-interface discipline) | 02, 14 |
| IMPL-NOTE-01 (rollback inference, planner-added) | 09, 13, 17 |
| NFR: unit coverage 80% (TS-RCV-4, D-RCV-40) | 15, 16, 17, 18, 20 |
| Security and authority (spec §Security and authority) | 08, 13 |

## Pre-submit checks

| Check | Result |
|---|---|
| Every scope bullet S1–S20 in `plan.md` maps to at least one TASK | YES (see `plan.md` §Scope) |
| Every in-scope SPEC-RWB-E1-043-001..010 maps to at least one TASK | YES (table above) |
| SPEC-RWB-E1-043-011, -012, -013, -014 left unmapped with an explicit reason | YES (spec.md's own coverage table does not tie any of them to a BR/AC/X row; -014/rollback is instead traced via spec.md §Feature flag and rollback, CLAR-008 and IMPL-NOTE-01) |
| No orphan TASK (each maps to ≥1 SPEC/FR and has a verification) | YES (00–21) |
| Every TASK has explicit `BLOCKED_BY` (`NONE` only for TASK-00) | YES |
| Every spec Requirement-to-SPEC coverage row (BR1-9, AC1-10, X1-7) is in `plan.md` §Requirement Logic To Task Coverage with no `BLOCKED` row | YES (20/20) |
| Every unit-test task is `BLOCKED_BY` its implementation task, names synthetic fixtures and a concrete command | YES (15←06/07/13, 16←08/10/13, 17←09/12/13, 18←11) |
| Unmapped effective-screen node groups | NONE — `NOT_APPLICABLE` (UI NO, 0 screens, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`) |
| Effective-screen consolidation task before release readiness | `NOT_APPLICABLE`; recorded in TASK-21 |
| Orphaned SPEC-* mappings / dangling references | NONE |
| Placeholder IDs (`DUMMY-*`, `TBD`, `TBA`) | NONE (`<seq>` in the migration filename is an explicitly-flagged merge-time value, not a placeholder left unexplained) |
| API tasks (spec `API_IMPACT: NEW_API_REQUIRED`) | TASK-13 (controllers), plus TASK-07/-08/-09/-10 (registry/service logic the controllers call); contract in `contracts/backend-apis.json` |
| Plan-approval preconditions | PRE-1 through PRE-8 **ALL PENDING**; enforced by TASK-00, with PRE-4/-5/-6 re-verified directly against `develop` by TASK-01 |
| Real PII, secrets, production data in plan outputs | NONE |
| Planner inferences beyond spec text are flagged, not asserted as fact | YES — IMPL-NOTE-01 (TASK-09, -13, -17) explicitly recommends FDA/Technical Specifier confirmation before Builder treats it as final |
