---
title: "Test scenarios — RWB-E1-044"
run_id: "INC-001-epic-1-RWB-E1-044"
story: "RWB-E1-044"
---

# Test scenarios — RWB-E1-044

Acceptance is the story business rules plus the story's remaining test cases (D-RCV-16, TS-RCV-7). `T-044-*` come from the spec; `P-044-*` are plan scenarios that verify existing SPEC items (no new behaviour). Data is synthetic (data-model §5, §6). Container tests carry `@Tag("recovery-it")` and run only in `recoveryIntegrationTest`; without Docker they fail. API Tester and Functional Automation Test: `NOT_APPLICABLE` (API NO, UI NO).

| ID | Covers | Level / Gradle task | Class | Task | Expected |
|---|---|---|---|---|---|
| T-044-01 (TC-E1-044-01) | BR1, BR5, BR6; SPEC-001, -003 | Container / `recoveryIntegrationTest` | `RecoveryFlywayIT` | TASK-11 | Empty `ace`: `V0001` applied once with checksum, no baseline row; 2nd run applies nothing |
| T-044-02 (TC-E1-044-02) | BR7; SPEC-012, -018; X1 | Container | `RecoveryFlywayIT` | TASK-11 | Comparator names the hand-added column; failure text `MSG-P3-016` `object=<table.column>`; no hand change → no difference |
| T-044-03 (TC-E1-044-03) | BR2; SPEC-002; X12; D-RCV-47, -48 | Container | `RecoveryFlywayIT` | TASK-11 | Objects only in the connection schema (`ace` / `rwb_it`); missing schema → migrate fails, `MSG-P3-016 schema=<name>`, no schema created, no `rwb_` object or recovery history anywhere |
| T-044-04 (TC-E1-044-04) | BR5; SPEC-003, -018; X2 | Container | `RecoveryFlywayIT` | TASK-11 | Edited applied file → validation fails, nothing applied, `MSG-P3-016 object=<version>` |
| T-044-05 (TC-E1-044-05) | BR2, guardrail; SPEC-007; X3, X10, X11 | Unit / `test` | `RecoveryMigrationLintTest` | TASK-08 | Every forbidden case of data-model §5 fails with file, line, rule; every allowed case passes (incl. REVIEW-022 cases) |
| T-044-06 (TC-E1-044-06) | BR3; SPEC-008; X4 | Unit | `RecoveryMigrationLintTest` | TASK-08 | Failures name all files involved; valid fix pair passes |
| T-044-07 (TC-E1-044-07) | BR4; SPEC-003, -009; X5a, X5b | Unit + container | `RecoveryMigrationLintTest`, `RecoveryFlywayIT` | TASK-08, TASK-11 | Lint fails on `U0001__x.sql`, `u0001__x.sql`, `R__x.sql`; `clean()` refused with Flyway's own message; no object changes |
| T-044-08 | SPEC-010; X6 | Container | `RecoveryFlywayIT` | TASK-11 | 2nd statement fails → no object from statement 1, no history row, run fails |
| T-044-09 | SPEC-011; X7 | Container | `RecoveryFlywayIT` | TASK-11 | Two concurrent migrates of `slow` → applied exactly once |
| T-044-10 | SPEC-009; X4 | Unit | `RecoveryMigrationLintTest` | TASK-08 | `V1__x.sql`, `V0001__x.sql`, duplicate `V0002`, gap `0001,0003` fail; empty and missing folder pass |
| T-044-11 | SPEC-004 (a); X8 | Unit (`ApplicationContextRunner`) / `test` | `RecoveryFlywayConfigTest` | TASK-06 | H2 URL → no `recoveryFlyway`, context starts, INFO skip line |
| T-044-12 | SPEC-005, -018; X9 | Spring + container | `RecoveryMigrationJobIT` | TASK-12 | Resolved `spring.flyway.enabled=false`, `spring.quartz.auto-startup=false`, `recovery.flyway.migrate-and-exit=true`; applies and exits 0; failing → exit 1; H2/no bean → ERROR `object=recoveryFlyway`, exit 1, nothing migrated; no schema created. "Core Flyway bean absent, Quartz not started" verified by substitution: resolved `spring.flyway.enabled=false` / `spring.quartz.auto-startup=false` plus the `AppConfig` `@ConditionalOnProperty("spring.flyway.enabled")` on the three core beans (lines 176–219, re-checked in TASK-01) |
| T-044-13 | SPEC-014; NFR-027 | Container | `RecoveryFlywayIT` | TASK-11 | DB at 2, classpath at 1 → succeeds, nothing applied or undone |
| T-044-14 | SPEC-019 | Build / `test` | whole ACE suite incl. `ModulithTest` | TASK-01, TASK-14 | No new failure vs the `develop` baseline; pre-existing failures reported, not fixed |
| T-044-15 | SPEC-004 (d); D-RCV-45 | Spring + container | `RecoveryMigrationJobIT` | TASK-12 | Profile `db-migrate` only → no bean, no initializer, no recovery history, no `rwb_` object, no schema created |
| T-044-16 | SPEC-003; BR6; D-RCV-48 | Container | `RecoveryFlywayIT` | TASK-11 | Pre-populated `ace`: baseline `0` then `V0001` `success=true`; core objects unchanged; 2nd migrate applies nothing |
| P-044-01 | SPEC-004 (b); REVIEW-024 | Spring + container | `RecoveryMigrationJobIT` | TASK-12 | Local start with a core initializer that cleans then migrates: `rwb_` fixture and `V0001` row exist after start; same without a core bean; control: bean-definition order puts the recovery initializer before the core one (`RecoveryFlywayConfig` first source), `WebApplicationType.NONE` |
| P-044-02 | SPEC-001, -003; CON-001 | Unit | `RecoveryFlywayConfigTest` | TASK-06 | `configure()` settings equal CON-001 (location, table, `createSchemas=false`, clean disabled, validate, `outOfOrder=false`, baseline `0`/on-migrate, naming validation, `*:future`, no schemas, no placeholders) |
| P-044-03 | SPEC-004 (a)(c)(d) | Unit (`ApplicationContextRunner`) | `RecoveryFlywayConfigTest` | TASK-06 | Data-model §3 truth table holds for bean, initializer and runner, incl. `db-migrate` + `MAE=true` without `db-migrate-recovery` → nothing; lazy contexts with a recording exit seam, presence by bean definition only (no `migrate()`, default exit seam never reached) |
| P-044-04 | SPEC-005; X9 | Unit | `RecoveryFlywayConfigTest` | TASK-06 | Runner built directly with stub Flyway and recording exit: success 0; `FlywayException` 1 with `MSG-P3-016`; no bean / not PG → 1, `object=recoveryFlyway`, migrate not called; switch not `true` → 1, `object=recoveryFlyway` (reason names the switch), migrate not called |
| P-044-07 | SPEC-001, -004 (b), -005, -018; REVIEW-037 | Unit | `RecoveryFlywayConfigTest` | TASK-06 | Every `RecoveryFlywayConfig` factory method called directly with stubs: `recoveryFlyway` settings equal `configure(...)`; initializer (given a `MockEnvironment` with synthetic `spring.datasource.url`, as TASK-04 reads it) resolves core first when present, calls `migrate()` once, reports and rethrows `FlywayException`; runner bean behaves as P-044-04 |
| P-044-05 | SPEC-018; CLAR-004 A | Unit | `RecoveryFlywayConfigTest` | TASK-06 | Report line has ID, `schema`, `object`, reason; no URL host, user or password |
| P-044-06 | SPEC-015; TS-RCV-3 | Build | `recoveryIntegrationTest` with the Docker daemon stopped, no host pinned in `~/.testcontainers.properties`; plus grep for `disabledWithoutDocker`/`Assumptions`/`assumeTrue` | TASK-14 | Task fails with "Could not find a valid Docker environment", none skipped; grep finds nothing |
| TC-E1-044-10 | Access | — | — | — | Deferred with the job monitor (CLAR-002 A); not run |
| HV-1..HV-3 | BR7 run rule; OPEN-019; CI | Human verification | — | TASK-17 | See `plan.md` §Functional Test Scenarios; not executed tests |

Commands (in `ace-monorepo/backend/`, order as TASK-14): `./gradlew clean checkstyleMain checkstyleTest test`; `./gradlew recoveryCoverageReport` (unit gate, `test` data only, main class directory); `./gradlew recoveryIntegrationTest`; `./gradlew recoveryCoverageReport recoveryCoverageVerification` (combined gate).
