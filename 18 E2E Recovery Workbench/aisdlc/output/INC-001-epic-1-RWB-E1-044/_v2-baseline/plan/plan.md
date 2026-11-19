> **HISTORICAL — do not build from this file.** This run was written on 10 November 2026 under
> D-RCV-47 (schema `ace`, `rwb_` prefix). Document set v14 (16 November 2026) reinstates schema
> `recovery` and `${recoverySchema}` through D-RCV-35 and ADR-010. Re-run the spec and plan before
> build (`OPEN-036`). The implementation evidence for the two current stories is in
> `output/INC-003-...` and `output/INC-002-...`.

---
title: "Implementation Plan — RWB-E1-044 Database migrations versioned with parameterized schema names"
run_id: "INC-001-epic-1-RWB-E1-044"
story: "RWB-E1-044"
jira: "TB0001-1205"
status: "SUCCESS"
---

# Implementation Plan — RWB-E1-044 Database migrations versioned with parameterized schema names

Design Source: NOT_REQUIRED (`UI In Scope: NO`, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`).

| Field | Value |
|---|---|
| Story | RWB-E1-044 (Jira `TB0001-1205`, epic `TB0001-1162` Foundation#1) |
| RUN_ID | `INC-001-epic-1-RWB-E1-044` |
| Input spec | `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` (`status: SPECIFIED`, SPEC-RWB-E1-044-001..019, `SPEC_CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`, `REQUIREMENT_COVERAGE_RESULT: SUCCESS [MISSING_RULES: 0] [CONTRADICTIONS: 0]`) |
| Spec contracts | `specify/contracts/backend-apis.json` (CON-RWB-E1-044-001, -002), `specify/contracts/frontend-integrations.json` (no frontend contract) |
| Plan contracts | `plan/contracts/backend-apis.json`, `plan/contracts/frontend-integrations.json` (spec contracts plus the plan's class, property, task and dependency names) |
| Governing decisions | D-RCV-02, -05, -06, -07, -12, -15, -16, -18, -28, -34, -40, -43..-49; OPEN-007, OPEN-013 rulings; OPEN-029 (context synced, CTX-UPDATE-007) |
| Context read | `project-context.md`, `domain-context.md`, `backend-context.md` (§13, §13.3 items 1–6, CTX-TECH-BE-FW-10..13), `backend-standards.md` (BS-2.1..2.9), `testing-standards.md` (TS-RCV-1..9), `frontend-context.md` (no change), `.github/rules/*` |
| ACE baseline | `ace-monorepo` `develop` **9f450bbd** (read-only at plan time) |
| Prepared | 2026-11-10, Implementation Planner (agent run) |

## Plan approval preconditions (not met at plan time)

The plan is written but **not approved**. Implementation Builder must not start until every row below has a decision and a date. TASK-RWB-E1-044-00 checks them; every build task is `BLOCKED_BY` it.

| ID | Precondition | Owner | State on 2026-11-10 | Evidence when met |
|---|---|---|---|---|
| PRE-1 | Specification approval (backlog and specification gate) for RWB-E1-044 on Jira `TB0001-1205` | Product Owner Chitchaya Muanchonchana (D-RCV-46) | **APPROVED** 2026-11-10 (Jira `TB0001-1205` comment 1782880, 2026-11-10 12:53) | Decision and date in `docs/increments/INC-001-epic-1-RWB-E1-044.md` "Owners and approvals" with the Jira comment ID |
| PRE-2 | OPEN-027: Product Owner re-confirms on `TB0001-1205` that BR7 is met by the container comparison T-044-02, run before every MR that touches recovery migrations or `RecoveryFlywayConfig` (not in the CI `check`), per D-RCV-44 | Product Owner (recovery tech lead asks) | **APPROVED** 2026-11-10 (Jira `TB0001-1205` comment 1782880, 2026-11-10 12:53) | OPEN-027 moved to "Settled" with the Jira comment ID and date |
| PRE-3 | OPEN-030 (new): ACE approval of the new test dependency **Testcontainers PostgreSQL** (`org.testcontainers:testcontainers-postgresql`, version from the Spring Boot 4.2.0-M2 BOM, 2.0.5; D-RCV-07, D-RCV-44) and the RWB-E1-044 edits to the shared file `backend/build.gradle.kts` (test scope: `test`/`testE2E` tag filters, new `recoveryIntegrationTest` task, JaCoCo execution data and class directory) plus the new file `backend/src/main/resources/application-db-migrate-recovery.yaml`; and confirmation that OPEN-023's JaCoCo approval also covers RWB-E1-044 creating the plugin if it merges before RWB-TE-001 (D-RCV-40) | ACE tech lead / Pongchai Charoenrungrodkun (ACE and Recovery lead, as for OPEN-023) | **APPROVED** 2026-11-10 by the recovery tech lead (D-RCV-49); ACE confirms at the MR review into `develop` | OPEN-030 moved to "Settled" with the ruling and date |
| PRE-4 | OPEN-028: ACE tech lead check that the sample-module pattern (own Flyway bean, folder, history table in schema `ace`) holds for the recovery module (needed by "before the RWB-TE-001 / RWB-E1-044 build") | Pipat Saengow (ACE tech lead) | **APPROVED** 2026-11-10 (D-RCV-49; Teams 2026-11-10: "อิงจาก sample-module ได้เลย"); follow-up check stays in OPEN-028, not blocking | OPEN-028 moved to "Settled" |
| PRE-5 | Human disposition of spec gate 4 Low findings REVIEW-RWB-E1-044-022..-025 (fix in a `/specify` re-run or accept); see §Upstream review disposition for how the plan already handles each. Also the plan's one spec deviation (plan gate 1 REVIEW-RWB-E1-044-032): **SPEC-015 (a) names `spring-boot-testcontainers`; the plan does not add it**, because `AppConfig.mainDataSource` reads `DataSourceProperties` directly, so `@ServiceConnection` never reaches it (§Plan-time verification). Accept the deviation, or re-specify; either way SPEC-015 (a) is corrected the next time `/specify` runs | Recovery tech lead (Jesniphat Pukkham) | **APPROVED** 2026-11-10: PRE-5 approved by the recovery tech lead (Jesniphat Pukkham), 2026-11-10: REVIEW-RWB-E1-044-022..-024 accepted as carried into tasks as written; REVIEW-RWB-E1-044-025 stays in OPEN-019 (DB role checked at the first DEV deploy), not a plan blocker; SPEC-015 (a) deviation accepted: no `spring-boot-testcontainers`, only `testcontainers-postgresql` as approved in D-RCV-49; no `/specify` re-run | Disposition recorded in `specify/compliance-validation.md` §4 and the card |
| PRE-6 | Plan approval | Forward Deployed Architect (Jesniphat Pukkham, D-RCV-15) | **APPROVED** 2026-11-10 13:41 (increment card) | Decision and date in the increment card |
| PRE-7 | Task approval | Forward Deployed Engineer (Jesniphat Pukkham, D-RCV-15) | **APPROVED** 2026-11-10 13:41 (increment card) | Decision and date in the increment card |

If PRE-3 is refused, or changes the dependency, version or file list, the plan is re-run; the Builder does not substitute another library or tool. If a `/specify` re-run under PRE-5 changes any SPEC, the plan is re-run.

Not preconditions (tracked, owned outside this story): OPEN-019 (Jenkins second step, needed before the first recovery migration deploys, i.e. RWB-E1-042 or RWB-E1-001); OPEN-026 (Docker on ACE build agents; until then `recoveryIntegrationTest` runs on the developer machine, D-RCV-44); OPEN-018 (BA story text).

## Upstream review disposition

Spec gate 4 (`review/spec-gate-review-r4.md`, 2026-11-10): `REVIEW_STATUS: FAIL [LOW: 4]`, `REVIEW_BLOCKING: NO`. The `FAIL` status and all four findings stay visible; PRE-5 dispositioned them 2026-11-10 (accepted as below; -025 stays in OPEN-019). The plan handles each as follows, without changing a SPEC:

| Finding | Sev. | Plan handling until disposition |
|---|---|---|
| REVIEW-RWB-E1-044-022 | Low | (b)/(c) are consistent with SPEC-007 (5) as written (`COMMENT ON COLUMN` is a table position): TASK-08 adds the failing fixture `COMMENT ON COLUMN efs_x.c` and the failing `COMMENT ON COLUMN ace.rwb_x.c`, and the lint treats a two-part `COMMENT ON COLUMN` argument as `table.column`, a three-part one as schema-qualified. (a) SPEC-007 (5) checks "every **relation** in `FROM`, `JOIN` and `USING`"; `FROM`/`USING` that introduce no relation are not relation positions in PostgreSQL grammar. TASK-08 adds allowed fixtures `EXTRACT(YEAR FROM d)`, `SUBSTRING(x FROM 2)`, `TRIM(BOTH FROM x)`, `a IS DISTINCT FROM b`, `CREATE INDEX rwb_i ON rwb_t USING gin (c)`, `ALTER TABLE rwb_t ALTER COLUMN c TYPE int USING c::int`, `JOIN rwb_y USING (id)`. If the human rules otherwise, the plan is re-run. |
| REVIEW-RWB-E1-044-023 | Low | No task asserts SPEC-003's "re-baseline fails loudly" sentence; T-044-16 asserts only the first-run baseline. (b) is a `compliance-validation.md` text fix for `/specify`. No plan impact. |
| REVIEW-RWB-E1-044-024 | Low | SPEC-004 (b) (recovery initializer after the core one) had no test. The plan adds **P-044-01** (TASK-12): local start with a core-like initializer that cleans then migrates, run with and without a core bean; after start the `rwb_` fixture object and the `V0001` row exist. This verifies existing SPEC-004 (b); it adds no behaviour. |
| REVIEW-RWB-E1-044-025 | Low | Deployment-side. TASK-17 sends K. Tee the OPEN-019 note with the reviewer's acceptance check (owner of a `rwb_`/recovery history object equals the owner of a core table; `has_table_privilege('ACEAppRole_DEV', ...)`), to be recorded at the first DEV run of the recovery step. RWB-E1-044 deploys no recovery step. |

## Plan gate 1 remediation (2026-11-10)

Plan gate 1 (`review/plan-gate-review.md`): `FAIL`, Medium -026, -027, Low -028..-036. Fixed in this revision, before gate 2; no SPEC changes.

| Finding | Sev. | Fix in this plan |
|---|---|---|
| REVIEW-RWB-E1-044-026 | Medium | (Unit-gate scope narrowed in gate 2 remediation, REVIEW-037: main class directory only.) Option (a), no new decision. A **unit-only 80% gate** now blocks: TASK-14 builds a JaCoCo report from `test` execution data alone (no `recoveryIntegrationTest.exec` present) and fails if the unit-tested classes (all five main classes plus `MigrationLint`, `MigrationSqlScanner`) are below 80% on LINE, INSTRUCTION, BRANCH or METHOD. The combined gate `recoveryCoverageVerification` (`test` + `recoveryIntegrationTest`) stays and also blocks; it is the only gate for the container-test support classes `SchemaComparator` and `RecoveryPostgres`, which only container tests run. No build-file change beyond PRE-3. §Coverage, §Unit Test Applicability, TASK-14, TASK-16, data-model §7. |
| REVIEW-RWB-E1-044-027 | Medium | TASK-06 / P-044-03: every `ApplicationContextRunner` context registers a recording `RecoveryMigrationExit` and lazy initialisation (`LazyInitializationBeanFactoryPostProcessor`); presence is asserted with `getBeanFactory().containsBeanDefinition(...)`, never by getting the initializer or runner, so no `migrate()` runs against the stub. P-044-04 builds the runner directly with stubs. Rule: no test in the `test` task may reach the default exit seam (TASK-15 greps). |
| REVIEW-RWB-E1-044-028 | Low | Activation keyed on the profile: `recoveryFlyway ⇔ PG ∧ (DBMR ∨ (FE ∧ ¬DBM))`; initializer ⇔ `PG ∧ FE ∧ ¬DBM`; runner ⇔ `DBMR`, and the runner fails fast if `MAE` is not true. New P-044-03 row: `db-migrate` + `MAE=true`, no `db-migrate-recovery` → nothing. data-model §3, TASK-03, -05, -06, contract `activationRule`. |
| REVIEW-RWB-E1-044-029 | Low | TASK-12: `RecoveryFlywayConfig` is the first source, the test configuration second, so without the `ObjectProvider` call the recovery initializer would be created first; the test asserts that bean-definition order as the control. Every `SpringApplication` in `RecoveryMigrationJobIT` sets `WebApplicationType.NONE`. |
| REVIEW-RWB-E1-044-030 | Low | P-044-06: runtime evidence with the Docker daemon stopped and no `docker.host` in `~/.testcontainers.properties` (records "Could not find a valid Docker environment"), plus static grep evidence (no `disabledWithoutDocker`, `Assumptions`, `assumeTrue` in `recovery-it` classes). Builder records both. |
| REVIEW-RWB-E1-044-031 | Low | TASK-12 / scenarios T-044-12 state the substitution: "core Flyway bean absent / Quartz not started" is verified by the resolved properties plus the `AppConfig` `@ConditionalOnProperty("spring.flyway.enabled")` conditions (lines 176-219 at `develop`); TASK-01 re-checks them at branch time. |
| REVIEW-RWB-E1-044-032 | Low | Recorded as a spec deviation under PRE-5; accepted 2026-11-10 (no `/specify` re-run). |
| REVIEW-RWB-E1-044-033 | Low | Report input is the JDBC URL string (`spring.datasource.url` in Spring, the test's own URL in `RecoveryFlywayIT`); only `currentSchema` is parsed, never host or user; no `connection.getSchema()` fallback (when the URL has no `currentSchema`, `schema` is omitted). One package-private `RecoveryFlywayConfig.migrateOrReport(Flyway, String url)` is called by the initializer, the runner and `RecoveryFlywayIT` (T-044-03, -04). |
| REVIEW-RWB-E1-044-034 | Low | No change needed: `Traceability_Matrix.md` at `HEAD` (5720155 and later) and in the working tree both have CRLF on 427 lines. |
| REVIEW-RWB-E1-044-035 | Low | Card updated: stage line, "Output run", "Review findings" (CRLF kept). |
| REVIEW-RWB-E1-044-036 | Low | `rule=` everywhere; allowed fixtures added for `OVERLAY(x PLACING 'a' FROM 2)` and `a IS NOT DISTINCT FROM b`; `POSITION` dropped from the exemption list (`POSITION('a' IN x)` has no `FROM`); fixture header rule = line 1 matches the file's own key (`RWB-E1-998` for the `V0002` file); HV-1 points at `implement/unit-tests/backend/`. |

## Plan gate 2 remediation (2026-11-10)

Plan gate 2 (`review/plan-gate-review-2.md`): `FAIL`, Medium -037, Low -038..-040. Fixed in this revision, before gate 3; no SPEC changes.

| Finding | Sev. | Fix in this plan |
|---|---|---|
| REVIEW-RWB-E1-044-037 | Medium | Unit gate is now the **main class directory alone** (`build/classes/java/main/th/co/scb/ace/demo/recovery/**`), selected by directory, 80% on all four metrics from `test` data; lint tooling is a separate information figure and is gated by the combined gate. New **P-044-07** (TASK-06): unit tests call every `RecoveryFlywayConfig` factory method directly (`recoveryFlyway` with a stub `DataSource`, `recoveryFlywayMigrationInitializer` with a mock `Flyway` and core `ObjectProvider` present / absent, then `afterPropertiesSet()` on the returned initializer: core resolved first, `migrate()` called, `FlywayException` reported and rethrown; `recoveryMigrateAndExitRunner` with stubs and a recording exit seam), so the lazy `ApplicationContextRunner` cases are not the only coverage of the configuration class. §Coverage, §Unit Test Applicability, TASK-06, TASK-14, TASK-16, data-model §7, contract. |
| REVIEW-RWB-E1-044-038 | Low | TASK-13: `recoveryIntegrationTest` execution data is added in a form that creates no task dependency (`executionData(tasks["recoveryIntegrationTest"])`, the eager `Task` overload), never `tasks.named(...)`, a provider or `files(provider)`; check: `./gradlew recoveryCoverageReport --dry-run` does not list `recoveryIntegrationTest`. TASK-14 step 2 checks `recoveryIntegrationTest.exec` is absent before and after the unit report and saves that output. |
| REVIEW-RWB-E1-044-039 | Low | The runner's switch check reports `object=recoveryFlyway` (a SPEC-018 value), with the reason naming the switch; no new `object` value. |
| REVIEW-RWB-E1-044-040 | Low | `docs/decisions/INC-001-decisions.md` "Next free squad number" set to D-RCV-50. |

## Plan gate 3 disposition (2026-11-10)

Plan gate 3 (`review/plan-gate-review-3.md`): `REVIEW_STATUS: FAIL`, Low only (-041, -042), `REVIEW_BLOCKING: NO`. The `FAIL` status and both findings stay visible. Disposition by the recovery tech lead (Jesniphat Pukkham), 2026-11-10: fix both as the reviewer proposed. Both are **fixed after gate 3, not re-reviewed (Low only, wording)**; gate 4 is not run by the tech lead's decision.

| Finding | Sev. | Fix in this plan |
|---|---|---|
| REVIEW-RWB-E1-044-041 | Low | Unit-gate script: a listed main class file with no XML `<class>` entry fails the gate, unless the class has no code (`package-info`, an interface with no method bodies); excluded class names are printed and saved with the evidence. §Coverage, TASK-14 step 2, data-model §7. |
| REVIEW-RWB-E1-044-042 | Low | Gate 2 remediation (-037..-040) now recorded in `tasks.md` status paragraph, a `## Pre-submit checks` row and the increment card's "Plan and tasks" row. |
| Gate 3 Builder note (not a finding) | — | TASK-04 states the JDBC URL source: `Environment` injected into `recoveryFlywayMigrationInitializer`, read `spring.datasource.url`; P-044-07 passes the URL the same way (a `MockEnvironment` with `spring.datasource.url`). TASK-04, TASK-06, scenarios P-044-07, §Package and file layout (bean list). |

## Change scope (carried from spec)

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` (SCR-44 deferred, CLAR-002 A) |
| Logic In Scope | `YES` (recovery Flyway bean, activation, migrate-and-exit runner, lint, container comparison) |
| API In Scope | `NO` (`NO_API_CHANGE`; `GET /api/recovery/v1/admin/jobs?type=MIGRATION` deferred, D-RCV-12) |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
| Database | No production migration file. Recovery history table `flyway_schema_history_recovery` in schema `ace`, created by Flyway at the first recovery run (D-RCV-47, -48) |
| Feature flag | None. Rollback = redeploy previous tag (SPEC-014) or revert MR |

## Plan-time verification of spec "plan detail" items

| Item (spec) | Check run at plan time (2026-11-10) | Result | Plan decision |
|---|---|---|---|
| ACE baseline | `git log develop` in `ace-monorepo` | HEAD `9f450bbd`; no `th/co/scb/ace/demo/recovery` package; no `jacoco` in `backend/build.gradle.kts` | RWB-TE-001 (INC-002) not merged yet. TASK-01 re-checks at branch time; TASK-13 follows SPEC-015 (d) for whichever case holds |
| SPEC-015 (a): Testcontainers version | Spring Boot BOM `spring-boot-dependencies-4.2.0-M2.pom` | `testcontainers.version` 2.0.5, `flyway.version` 12.11.0, `postgresql.version` 42.7.13; `org.testcontainers:testcontainers-postgresql:2.0.5` in the Gradle cache; `spring-boot-testcontainers:4.2.0-M2` not cached | One line: `testImplementation("org.testcontainers:testcontainers-postgresql")` (BOM-managed, no version). Container class `org.testcontainers.postgresql.PostgreSQLContainer` (Testcontainers 2.x package) |
| SPEC-015 (a): `spring-boot-testcontainers` | `AppConfig.mainDataSource` is built from `DataSourceProperties` (`spring.datasource.*`) | `@ServiceConnection` supplies `JdbcConnectionDetails`, which `mainDataSource` does not read | **Not added.** Tests pass the container URL as `spring.datasource.*` / an explicit `DataSource`. One dependency fewer than the spec lists; recorded in OPEN-030 and as a spec deviation under PRE-5 (REVIEW-RWB-E1-044-032) |
| `testcontainers-junit-jupiter` | — | Not needed: containers are started in `@BeforeAll` without `@Testcontainers`, so a missing Docker throws and the test **fails** (TS-RCV-3), never skips | Not added |
| Container image | `docker info`; `docker images postgres` | Docker 29.8.2 on the planner's machine; `postgres:16-alpine` cached (ACE's local comment uses `postgres:16.8`) | `postgres:16-alpine`; the Builder records the image digest in evidence |
| SPEC-004 (a): H2 / PostgreSQL detection | `application.yaml`: default H2 URL (32), `scb-aks` and `db-migrate` URLs `jdbc:postgresql://…?currentSchema=ace` (224, 295) | URL prefix is known before any connection | Detection = `spring.datasource.url` starts with `jdbc:postgresql:` (no connection during condition evaluation). Anything else, or a missing URL, is "not PostgreSQL" |
| SPEC-005: migrate-and-exit switch name | spec "property name is a plan detail" | — | `recovery.flyway.migrate-and-exit: true`, set only in `application-db-migrate-recovery.yaml`. The runner is keyed on profile `db-migrate-recovery` (D-RCV-45; REVIEW-028), not on the property, so an environment variable cannot start it in the core step; under that profile the runner fails fast if the switch is not `true` |
| SPEC-004 (b), backend-context §13.3 item 2: order without hard `@DependsOn` | `SampleModuleConfig` uses `@DependsOn("coreFlywayMigrationInitializer")`, which fails when core is absent | — | Recovery initializer factory method takes `@Qualifier("coreFlywayMigrationInitializer") ObjectProvider<FlywayMigrationInitializer>` and calls `ifAvailable(...)` before building its own, forcing core migrate first only when core exists |
| §13.3 item 5: `cleanDisabled(true)` in every profile | — | — | Yes: set on the bean (SPEC-003) |
| SPEC-006: empty folder | Flyway 12 with a missing location only warns (`failOnMissingLocations` default false) | — | **No placeholder file.** The folder is created by the first migration story (RWB-E1-042). The lint treats a missing folder as empty (passes); the recovery step with no files only baselines |
| Profile override of `spring.flyway.enabled` | Spring Boot loads `application-{profile}.yaml` after `application.yaml` (incl. its profile documents) | Expected: the new file wins over the `db-migrate` document's `enabled: true` | TASK-12 (T-044-12) asserts the resolved values from the real `application.yaml` + new file. If they do not resolve as expected, the Builder stops and reports (no edit of `application.yaml` is allowed) |
| `testE2E` filter | `build.gradle.kts` lines 154–160 (`test`, `excludeTags("e2e")` at 157) and 161–172 (`testE2E`) | `testE2E` has an empty filter (runs every test) | Add `excludeTags("recovery-it")` to `testE2E` and add `"recovery-it"` to `test`'s `excludeTags("e2e")` |

## Scope

Each bullet maps to tasks in `tasks.md`.

| # | Scope bullet | TASK-* |
|---|---|---|
| S1 | Check plan-approval preconditions; branch; record `develop` SHA, RWB-TE-001 merge state, ACE `test` baseline, Docker | TASK-00, TASK-01 |
| S2 | Test dependency and Gradle test-task tag filters; `recoveryIntegrationTest` task | TASK-02 |
| S3 | `RecoveryFlywayConfig`: `configure(DataSource)` with every SPEC-001/-003 setting, `recoveryFlyway` bean, `RecoveryFlywayCondition` (activation truth table, H2 skip log) | TASK-03 |
| S4 | Local-start initializer ordered after core; MSG-P3-016 reporting of Flyway failures | TASK-04 |
| S5 | Migrate-and-exit runner, exit seam, `application-db-migrate-recovery.yaml` | TASK-05 |
| S6 | Unit tests of config, condition, reporting and runner (no database) | TASK-06 |
| S7 | Migration lint (test-scope tooling): schema, prefix, privilege, header, key, name, sequence, undo/repeatable rules | TASK-07 |
| S8 | `RecoveryMigrationLintTest` with a passing and a failing fixture per rule; real folder check | TASK-08 |
| S9 | `SchemaComparator` (test support) | TASK-09 |
| S10 | Container test support and synthetic migration fixtures | TASK-10 |
| S11 | `RecoveryFlywayIT`: container tests T-044-01..-04, -07 (clean), -08, -09, -13, -16 | TASK-11 |
| S12 | `RecoveryMigrationJobIT`: Spring + container tests T-044-12, -15, P-044-01 | TASK-12 |
| S13 | JaCoCo: `recoveryIntegrationTest` execution data and the migration tooling class directory | TASK-13 |
| S14 | Backend regression, `recoveryIntegrationTest` run (D-RCV-44 evidence) and 80% coverage gate | TASK-14 |
| S15 | Guardrails, deferred-scope exclusions and shared-file footprint check | TASK-15 |
| S16 | Unit Test Evidence table | TASK-16 |
| S17 | Release readiness: ACE commit/MR record, traceability, notices (OPEN-019 / K. Tee, INC-002 Builder) | TASK-17 |

## Backend Plan

Status: **REQUIRED** (SPEC-001..-016, -018, -019). All new Java types are package-private unless Spring needs otherwise, in `th.co.scb.ace.demo.recovery.casewf.internal.migration` (CLAR-003 A; no `package-info.java`).

### Package and file layout

| Path (under `ace-monorepo/backend/`) | Scope | Content |
|---|---|---|
| `src/main/java/th/co/scb/ace/demo/recovery/casewf/internal/migration/RecoveryFlywayConfig.java` | main | `@Configuration`; `static FluentConfiguration configure(DataSource)`; beans `recoveryFlyway`, `recoveryFlywayMigrationInitializer`, `recoveryMigrateAndExitRunner` |
| `.../migration/RecoveryFlywayCondition.java` | main | Spring `Condition` implementing the activation truth table (data-model §3) for `recoveryFlyway`, with nested `RecoveryLocalStartCondition` for the initializer; logs the H2 skip at INFO |
| `.../migration/RecoveryMigrateAndExitRunner.java` | main | `InitializingBean`; migrate-and-exit (SPEC-005, X9) |
| `.../migration/RecoveryMigrationExit.java` | main | Functional exit seam; default = `System.exit(SpringApplication.exit(context, () -> code))`, as `AppConfig.flywayMigrationStrategy` |
| `.../migration/RecoveryMigrationReport.java` | main | Formats and logs `MSG-P3-016` with `schema`/`object` parameters and the Flyway reason (SPEC-018); no message text |
| `src/main/resources/application-db-migrate-recovery.yaml` | main (new file) | `spring.flyway.enabled: false`, `spring.quartz.auto-startup: false`, `recovery.flyway.migrate-and-exit: true` |
| `src/test/java/.../migration/MigrationLint.java`, `MigrationSqlScanner.java` | test tooling | Lint rules (SPEC-007..-009) and comment/dollar-quote-aware tokenizer |
| `src/test/java/.../migration/SchemaComparator.java` | test tooling | SPEC-012 |
| `src/test/java/.../migration/RecoveryPostgres.java` | test tooling | One container per test class, fresh database per test, schema setup, pre-populated `ace` |
| `src/test/java/.../migration/RecoveryFlywayConfigTest.java`, `RecoveryMigrationLintTest.java` | test (`test` task) | Unit tests, no database |
| `src/test/java/.../migration/RecoveryFlywayIT.java`, `RecoveryMigrationJobIT.java` | test (`recoveryIntegrationTest`, `@Tag("recovery-it")`) | Container tests |
| `src/test/resources/recovery-migration-lint/<case>/*.sql` | test resource | Lint fixtures (synthetic DDL) |
| `src/test/resources/recovery-migration-fixtures/<case>/*.sql` | test resource | Container migration fixtures (synthetic DDL, `rwb_` names) |
| `build.gradle.kts` | shared (PRE-3) | One `testImplementation` line; tag filters; `recoveryIntegrationTest`; JaCoCo wiring (TASK-13) |

Not created: `db/modulemigration/recovery/` folder or any file in it (first migration story creates it), `package-info.java`, any controller, entity, repository, `MigrationRunRecorder`. Not edited: `AppConfig.java`, `application.yaml`, `SampleModuleConfig.java`, security config, CI files, frontend.

### Bean design

- `configure(DataSource ds)` returns `Flyway.configure().dataSource(ds).locations("classpath:db/modulemigration/recovery").table("flyway_schema_history_recovery").createSchemas(false).cleanDisabled(true).validateOnMigrate(true).outOfOrder(false).baselineVersion("0").baselineOnMigrate(true).validateMigrationNaming(true)`; no `schemas`, `defaultSchema`, `placeholders`, `ignoreMigrationPatterns` or `mixed` call (Flyway defaults `*:future`, `mixed=false`). The bean is `configure(mainDataSource).load()`. Container tests use the same `configure(...)` and override only `locations(...)` to a fixture folder, so every other setting under test is the production one.
- `recoveryFlyway`: `@Bean @Conditional(RecoveryFlywayCondition.class)`, parameter `@Qualifier("mainDataSource") DataSource`.
- `recoveryFlywayMigrationInitializer`: `@Conditional(RecoveryLocalStartCondition)` = `PG ∧ FE ∧ ¬DBM` (local start only; never under any `db-migrate` profile); forces the core initializer first via `ObjectProvider` (see plan-time table); its strategy calls `migrateOrReport(flyway, url)`, where `url` is `environment.getProperty("spring.datasource.url")` from the `Environment` injected into the factory method (gate 3 Builder note), and rethrows the `FlywayException` (local start fails). The condition is a nested class of `RecoveryFlywayCondition`; both share one evaluation helper.
- `recoveryMigrateAndExitRunner`: `@Profile("db-migrate-recovery")` only, **not** conditional on `recoveryFlyway` (SPEC-005) and not on the property (REVIEW-028). Takes `@Qualifier("recoveryFlyway") ObjectProvider<Flyway>`, the `Environment` and `ObjectProvider<RecoveryMigrationExit>`. In `afterPropertiesSet()`: `recovery.flyway.migrate-and-exit` not `true` → `MSG-P3-016 object=recoveryFlyway` at ERROR with the reason naming the switch, exit 1, no migrate (SPEC-018 object values; REVIEW-039); bean absent or URL not PostgreSQL → `MSG-P3-016 object=recoveryFlyway` at ERROR, exit 1, no migrate; else `migrateOrReport(...)` → exit 0; `FlywayException` → exit 1. Runs during bean initialisation, before any `SmartLifecycle` start.
- `static void migrateOrReport(Flyway, String jdbcUrl)` (package-private, in `RecoveryFlywayConfig`): calls `migrate()`; on `FlywayException` logs through `RecoveryMigrationReport` and rethrows. The initializer, the runner and `RecoveryFlywayIT` (T-044-03, -04) all call it, so container tests exercise the production reporting path (REVIEW-033).
- `MSG-P3-016` parameter `schema`: the `currentSchema` parameter parsed from the JDBC URL string passed in (`spring.datasource.url` in Spring; the test's own URL in `RecoveryFlywayIT`); only `currentSchema` is read, never host, user or password; if the URL has none, `schema` is omitted (no connection is opened for it); omitted for lint. `object`: Flyway version (checksum / failed migration), `recoveryFlyway` (also for the runner's switch check), or `file`/`file:line` (lint): only the SPEC-018 values.

### Lint design (SPEC-007..-009; test scope, no database)

- Input: every file in a folder (real: `src/main/resources/db/modulemigration/recovery`, path relative to the Gradle project dir; missing = empty = pass; fixtures: `src/test/resources/recovery-migration-lint/<case>`).
- `MigrationSqlScanner` removes `--` and `/* */` comments (keeping line numbers), keeps single-quoted literals as opaque tokens except the arguments of `nextval`/`currval`/`setval` and `'…'::regclass`, and re-scans dollar-quoted bodies with the same rules.
- `MigrationLint` returns all failures of a folder in one result, each `MSG-P3-016 object=<file>[:<line>] rule=<code>`; the test asserts the ID, object and rule code, not wording. Rules exactly as SPEC-007 (1)–(6), SPEC-008, SPEC-009, with the position list and allow-list of SPEC-007 (5) and CON-002, plus the REVIEW-022 handling above.
- Fixture matrix: `data-model.md` §5 and `tests/scenarios.md` (every forbidden and allowed case of T-044-05 one file or one line each).

### Container tests design

- `RecoveryPostgres` starts one `postgres:16-alpine` container per test class in `@BeforeAll` (no `@Testcontainers`, no `disabledWithoutDocker`), and gives each test a fresh database (`CREATE DATABASE rwb_it_<n>`) so every case starts clean. Test setup, never Flyway, creates schemas (`ace`, `rwb_it`). JDBC URL `…/rwb_it_<n>?currentSchema=<schema>`. Credentials are the container's generated ones (SPEC-016).
- "Pre-populated `ace`" (T-044-12, -15, -16): test setup creates `core_fixture(id int)` and a core-like `flyway_schema_history` with one synthetic row before any recovery migrate.
- Spring + container tests (`RecoveryMigrationJobIT`) start a `SpringApplication` with sources `RecoveryFlywayConfig` (first) + a test configuration (second) only (no auto-configuration, no `AppConfig`), `WebApplicationType.NONE` on every one (REVIEW-029), so the real `application.yaml` and `application-db-migrate-recovery.yaml` are resolved with the given profiles. The container URL is passed as command-line arguments (`--spring.datasource.url=…`), which outrank profile files. The test configuration provides `mainDataSource`, a recording `RecoveryMigrationExit`, and, where a fixture must be applied, overrides `recoveryFlyway` with `configure(ds).locations(<fixture>).load()` (`spring.main.allow-bean-definition-overriding=true` in that test only). Bean presence under each profile set is asserted without the override.

### Coverage (SPEC-015 (d), D-RCV-40, D-RCV-43)

- Case A (expected; RWB-TE-001 merged first): `recoveryCoverageReport` / `recoveryCoverageVerification` exist. Add `recoveryIntegrationTest` to their `executionData` and `mustRunAfter`; add class directory `sourceSets.test.output` filtered `th/co/scb/ace/demo/recovery/casewf/internal/migration/**` excluding `**/*Test.class`, `**/*Test$*.class`, `**/*IT.class`, `**/*IT$*.class`. Nothing else in them changes.
- Case B (RWB-E1-044 merges first): create the `jacoco` plugin (`toolVersion = "0.8.14"`) and both tasks in the SPEC-015 (d) shape: main output filtered `th/co/scb/ace/demo/recovery/**` plus the class directory above, `executionData` from `test` and `recoveryIntegrationTest`, BUNDLE rules COVEREDRATIO ≥ 0.80 for LINE, INSTRUCTION, BRANCH, METHOD, XML + HTML, not wired to `check`/`build`. RWB-TE-001 then adds only its tooling class directory (D-RCV-43 (2)).
- Two blocking gates, each 80% on LINE, INSTRUCTION (statements), BRANCH and METHOD (functions); no exclusion beyond the filters above (REVIEW-026, implementation-execution-gates: integration coverage does not replace unit coverage):
  1. **Unit gate, main scope** (`test` execution data only; REVIEW-026, -037, -038). After `./gradlew clean … test` and before `recoveryIntegrationTest`, with `build/jacoco/recoveryIntegrationTest.exec` absent (checked before **and** after the report, output saved), run `./gradlew recoveryCoverageReport` and save its XML/HTML as the unit report. Scope is chosen **by directory, not by name**: every class whose `.class` file is under `build/classes/java/main/th/co/scb/ace/demo/recovery/` (the main class directory of the bundle). The Builder's short stdlib script lists those class files, maps each to its XML `<class name=…>`, sums their LINE, INSTRUCTION, BRANCH, METHOD `<counter>` values and fails if any is below 80%. If a listed class file has no XML `<class>` entry the script fails, unless the class has no code (for example `package-info`, or an interface with no method bodies); the script prints those excluded class names, and that output is saved with the evidence (REVIEW-041). Test-scope tooling is not added to this figure. The same script prints the lint tooling (`MigrationLint`, `MigrationSqlScanner`, under `build/classes/java/test/…/migration/`) as its own figure for information; it is gated by the combined gate. `recoveryCoverageVerification` is not run on this report (the container-support classes would fail it by design). Execution-data wiring (TASK-13) must add no task dependency: `./gradlew recoveryCoverageReport --dry-run` must not list `recoveryIntegrationTest`.
  2. **Combined gate** (`test` + `recoveryIntegrationTest`): `recoveryCoverageVerification` as the spec shapes it, over every class in the two class directories; it is the gate for `SchemaComparator` and `RecoveryPostgres`.

### Checkstyle

ACE CI runs `backend:check` incl. `checkstyleMain` and `checkstyleTest` (13.5.0, LineLength 100). All new main and test Java files pass it; long SQL fixture strings live in fixture files, not Java. Pre-existing ACE checkstyle failures are reported, not fixed.

## Frontend Plan

Status: **NOT_APPLICABLE** (SPEC-017; `UI In Scope: NO`, `Frontend Changes Required: NO`). Evidence: the only UI touchpoint, SCR-44, is deferred (CLAR-002 A, D-RCV-12); `ace-monorepo/frontend/` has no recovery folder from this story. No frontend implementation, unit-test or coverage task. TASK-15 checks that no file under `frontend/` changes.

## Integration and cross-layer

No API, no frontend consumer, no backend contract consumed by a frontend task. The backend-only contracts are CON-RWB-E1-044-001 (Flyway module configuration) and -002 (migration file convention). Cross-environment integration is the Jenkins second step (OPEN-019, outside the repository; not built or run here).

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Trace | Reason | Tasks |
|---|---|---|---|---|---|---|
| Backend | YES | REQUIRED | 80% LINE, INSTRUCTION, BRANCH, METHOD, two blocking gates (§Coverage): (1) unit gate from `test` execution data alone on the main class directory `th/co/scb/ace/demo/recovery/**` (selected by directory); (2) `recoveryCoverageVerification` on main `th/co/scb/ace/demo/recovery/**` + test tooling `th/co/scb/ace/demo/recovery/casewf/internal/migration/**` (excl. `*Test`, `*IT`), execution data `test` + `recoveryIntegrationTest` | SPEC-001..-016, -018, -019; FR-RWB-001, FR-RWB-020, NFR-RWB-006 | New bean, condition, runner, reporting; lint and comparator tooling | TASK-06, -08, -11, -12; gate TASK-14; evidence TASK-16 |
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | SPEC-017 | No frontend change (SCR-44 deferred, CLAR-002 A) | None (TASK-15 checks no `frontend/` diff) |

## Requirement Logic To Task Coverage

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| BR1 | SPEC-001, -005, -006, -016 | TASK-03, TASK-05, TASK-11, TASK-12, TASK-15 | DIRECT_IMPLEMENTATION | T-044-01, T-044-12, T-044-16; footprint check (only recovery bean writes `rwb_`/recovery history) | COVERED |
| BR2 | SPEC-002, -007 | TASK-03, TASK-07, TASK-08, TASK-11 | DIRECT_IMPLEMENTATION | T-044-03 (same file lands only in connection schema; missing schema fails, nothing created), T-044-05 | COVERED |
| BR3 | SPEC-006, -008, -009 | TASK-07, TASK-08 | DIRECT_IMPLEMENTATION | T-044-06, T-044-10 | COVERED |
| BR4 | SPEC-003, -009, -010, -014 | TASK-03, TASK-07, TASK-08, TASK-11 | DIRECT_IMPLEMENTATION | T-044-07 (lint `U*`/`R__`; clean refused), T-044-08, T-044-13; P-044-02 settings | COVERED |
| BR5 | SPEC-003, -005 | TASK-03, TASK-05, TASK-11, TASK-12 | DIRECT_IMPLEMENTATION | T-044-04 (edited file stops run), T-044-12 (job validates on run) | COVERED |
| BR6 | SPEC-001, -003 | TASK-03, TASK-11 | DIRECT_IMPLEMENTATION | T-044-01, T-044-16 (own history table, baseline 0 on non-empty `ace`, core history unchanged) | COVERED |
| BR7 | SPEC-012 | TASK-09, TASK-11, TASK-14, TASK-17 | DIRECT_IMPLEMENTATION | T-044-02; `recoveryIntegrationTest` result attached to `implement/` before the MR (D-RCV-44); PRE-2 (OPEN-027) | COVERED |
| Flow 1 | SPEC-006 | TASK-07, TASK-08 | DIRECT_IMPLEMENTATION | T-044-06, T-044-10 (name/header rules); real-folder lint pass | COVERED |
| Flow 2 | SPEC-007, -008, -009 | TASK-07, TASK-08, TASK-14 | DIRECT_IMPLEMENTATION | T-044-05, -06, -07, -10 in the ACE `test` task (no pipeline step, D-RCV-05) | COVERED |
| Flow 3 | SPEC-011, -012, -015 | TASK-02, TASK-10, TASK-11, TASK-14 | DIRECT_IMPLEMENTATION | `recoveryIntegrationTest` on Testcontainers PostgreSQL; fails without Docker (P-044-06) | COVERED |
| Flow 4 | SPEC-012 | TASK-09, TASK-11 | DIRECT_IMPLEMENTATION | T-044-02 (two clean container databases; real-environment gate parked, CLAR-001 A) | COVERED |
| Flow 5–6 | SPEC-003, -004, -005 | TASK-03, TASK-04, TASK-05, TASK-11, TASK-12 | DIRECT_IMPLEMENTATION | T-044-01, -04, -12, P-044-01 (local start order) | COVERED |
| Flow 7 | SPEC-013 | TASK-15 | DIRECT_IMPLEMENTATION (exclusion check) | Diff has no `MigrationRunRecorder`, no `/admin/jobs`, no SCR-44 (deferred, CLAR-002 A) | COVERED |
| §12 Contract | SPEC-013 | TASK-15 | DIRECT_IMPLEMENTATION (exclusion check) | As Flow 7 | COVERED |
| §13 step 2 | SPEC-006 | TASK-15 | DIRECT_IMPLEMENTATION (exclusion check) | Diff has no file in `db/modulemigration/recovery/` (baseline is RWB-E1-001) | COVERED |
| §14 MSG-P3-016 | SPEC-018 | TASK-04, TASK-05, TASK-06, TASK-07, TASK-11, TASK-12 | DIRECT_IMPLEMENTATION | P-044-05 (format), T-044-02/-03/-04/-08/-12 assert ID + parameters; refused clean shows Flyway's message (T-044-07) | COVERED |
| X-paths (direct) | SPEC-003, -009 | TASK-07, TASK-08, TASK-11 | DIRECT_IMPLEMENTATION | T-044-07 (`U*.sql` refused), T-044-04 (checksum stop) | COVERED |
| X-paths (inherited) | SPEC-010, -011 | TASK-11 | INHERITED_EXISTING_BEHAVIOR | T-044-08 (rollback), T-044-09 (advisory lock, applied once) | COVERED |
| §10 Authority | SPEC-005, -013 | TASK-05, TASK-07, TASK-15, TASK-17 | DIRECT_IMPLEMENTATION | No endpoint / role check in diff; lint bans `GRANT`/`REVOKE` (T-044-05); OPEN-019 role note to K. Tee (REVIEW-025 check) | COVERED |
| Guardrails | SPEC-007, -016, -019 | TASK-07, TASK-08, TASK-10, TASK-14, TASK-15 | DIRECT_IMPLEMENTATION | T-044-05 (schema, prefix incl. `FROM`/`JOIN`, privileges); fixture/PII/secret grep; T-044-14 | COVERED |
| NFR-027 | SPEC-014 | TASK-03, TASK-11 | DIRECT_IMPLEMENTATION | T-044-13 (`*:future` ignored, `outOfOrder(false)`) | COVERED |
| Precondition | SPEC-001 | TASK-01, TASK-03, TASK-14 | DIRECT_IMPLEMENTATION | Package `recovery.casewf.internal.migration` only, no `package-info`; `ModulithTest` and (if merged) RWB-TE-001 boundary tests green | COVERED |

Exception rows (spec §Exceptional-case behaviour): X1 → TASK-11 (T-044-02); X2 → TASK-11 (T-044-04); X3 → TASK-08 (T-044-05); X4 → TASK-08 (T-044-06, -10); X5a → TASK-11 (T-044-07); X5b → TASK-08 (T-044-07); X6 → TASK-11 (T-044-08); X7 → TASK-11 (T-044-09); X8 → TASK-06 (T-044-11, P-044-03); X9 → TASK-06 (P-044-04), TASK-12 (T-044-12); X10 → TASK-08 (T-044-05); X11 → TASK-08 (T-044-05); X12 → TASK-11 (T-044-03).

Resolved clarifications carried: CLAR-001 A → TASK-09/-11 (BR7 on container comparison; no flag, no read-only account); CLAR-002 A → TASK-15 (deferred parts absent); CLAR-003 A → TASK-03 (package only, no `package-info`); CLAR-004 A → TASK-04/-05/-07 (ID + parameters, no text); CLAR-005 (D-RCV-47/-48) → TASK-03/-07/-11; CLAR-006 → TASK-07/-08; CLAR-007 → TASK-05/-17 (Jenkins step OPEN-019); CLAR-008 → TASK-03/-06; CLAR-009 → TASK-15; CLAR-010 → TASK-11 (Flyway's own clean message).

## Functional Test Scenarios

| Scenario | Owner | Applicability | Note |
|---|---|---|---|
| API scenarios | API Tester | NOT_APPLICABLE | `API In Scope: NO`, `NO_API_CHANGE`; card lists API Tester "Not used" |
| UI workflow scenarios | Functional Automation Test | NOT_APPLICABLE | `UI In Scope: NO`; card lists FAT "Not used" |
| HV-1: the MR's `recoveryIntegrationTest` result is attached before merge (D-RCV-44) | Human verification (recovery tech lead, PR approval) | Gap requiring human verification | CI does not run it until OPEN-026; reviewer checks the `recoveryIntegrationTest` XML and console in `implement/unit-tests/backend/` against the MR head SHA |
| HV-2: first DEV run of the Jenkins recovery step (OPEN-019): exit 0, `flyway_schema_history_recovery` baseline row 0, owner/privilege check of REVIEW-025 | Human verification (K. Tee with recovery tech lead) | Gap requiring human verification; happens at RWB-E1-042 / RWB-E1-001 deploy | Not executed in this story |
| HV-3: GitLab MR pipeline `test` job green incl. `RecoveryMigrationLintTest`, `RecoveryFlywayConfigTest`, `ModulithTest` | Human verification | Gap requiring human verification | Read the MR pipeline log |

All acceptance (D-RCV-16, TS-RCV-7) is unit and container level: see `tests/scenarios.md`.

## Screen-to-task mapping

`NOT_APPLICABLE`: `UI In Scope: NO`, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`, 0 screens (SCR-44 deferred). No visual-fidelity, screenshot or component-inventory task; `plan/frontend/components.md` not created (agent rule for UI NO).

## Security, privacy, compliance

- Authentication / authorization: no endpoint, no method security (spec Backend Specification). Audit, KYC/AML, suitability, consent, maker-checker: not applicable (no business data, no case decision).
- Least privilege: recovery migrations contain no `GRANT`/`REVOKE` (lint); the Jenkins step uses the core step's role (OPEN-019 condition; REVIEW-025 check is HV-2).
- Data protection: fixtures are synthetic DDL only; container credentials are generated; no connection string, credential or token in config, tests or evidence (SPEC-016). TASK-15 greps the diff.
- Never run against a shared database (TS-RCV-8, BS-2.5): container tests only; the Builder never sets `spring.datasource.url` to a shared host and never runs the `db-migrate*` profiles against a real environment.
- Shared-file discipline: only `backend/build.gradle.kts` (PRE-3) is edited among shared files; TASK-15 compares `git diff --name-only` with the layout table.

## Risks

| Risk | Mitigation | Task |
|---|---|---|
| PRE-3 refused or changed | Re-run planner; no substitution | TASK-00 |
| RWB-TE-001 merges between plan and branch, or after branch | TASK-01 records state; TASK-13 Case A/B; rebase before MR re-checks | TASK-01, TASK-13 |
| Profile file does not override `db-migrate`'s `spring.flyway.enabled: true` | T-044-12 asserts resolved values; stop and report (no `application.yaml` edit) | TASK-12 |
| Docker image pull blocked on the SCB network | `postgres:16-alpine` cached locally; Builder records digest; if unavailable, stop (tests must fail, not skip) | TASK-01, TASK-14 |
| Lint misreads valid SQL (REVIEW-022) | Allowed fixtures for non-relation `FROM`/`USING`; PRE-5 disposition | TASK-08 |
| Local start: ACE core `clean()` drops `rwb_` objects (REVIEW-024) | Initializer forced after core; P-044-01 | TASK-04, TASK-12 |
| Pre-existing ACE `test` failure on `develop` | Baseline in TASK-01; reported, not fixed (T-044-14) | TASK-01, TASK-14 |
| JaCoCo agent slows `test` | Record durations vs baseline | TASK-14 |

## Out of scope

Table definitions and Physical Schema v4 baseline (RWB-E1-001); reference data (RWB-E1-043); code owners and browser runner (RWB-TE-002); deployment slots (DL34, DL35); the Jenkins job change (OPEN-019); any schema creation or DBA grant (D-RCV-47); real-environment drift gate and flag `rwb.p3.migration-drift-gate` (D-RCV-05, CLAR-001 A); `MigrationRunRecorder`, `GET /api/recovery/v1/admin/jobs?type=MIGRATION`, SCR-44, MSG-P4-002, TC-E1-044-10 (CLAR-002 A); CI wiring of `recoveryIntegrationTest` (OPEN-026).

## Status reporting

```text
PLANNER_STATUS_SUMMARY: Plan and 18 tasks for RWB-E1-044 (recovery Flyway bean, profile-keyed activation, migrate-and-exit runner, lint, container tests, main-scope unit and combined JaCoCo gates); backend only; plan gate 1 findings -026..-036 and gate 2 findings -037..-040 remediated 2026-11-10; gate 3 Low -041, -042 fixed after gate 3, not re-reviewed (Low only, wording); PRE-1..PRE-4 approved; PRE-5 approved 2026-11-10; plan approval waits on a non-blocking plan gate and FDA/FDE approval (PRE-6, PRE-7).
PLANNER_STATUS_DETAIL: SUCCESS [REASON: SPEC-001..019 mapped; 22/22 coverage rows COVERED; PRE-6, PRE-7 pending, enforced by TASK-00] [UNBLOCK_ACTION: recovery tech lead approves plan (PRE-6) and tasks (PRE-7) after a non-blocking plan gate]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: n/a]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: All 22 spec coverage rows (7 business rules, flows, contract, message, X-paths, authority, guardrails, NFR-027, precondition) mapped to tasks and tests; no blocked row.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 22] [TASK_COVERED_RULES: 22] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
```
