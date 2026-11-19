---
title: "Plan gate review 2 — RWB-E1-044"
run_id: "INC-001-epic-1-RWB-E1-044"
story: "RWB-E1-044"
jira: "TB0001-1205"
review_type: "PLAN_GATE_REVIEW (gate 2)"
reviewer: "Compliance Reviewer (subagent of Implementation Planner)"
date: "2026-11-10"
---

# Plan gate review 2 — RWB-E1-044

Scope: the revised `output/INC-001-epic-1-RWB-E1-044/plan/` (plan.md, tasks.md, data-model.md, tests/scenarios.md, contracts/backend-apis.json, contracts/frontend-integrations.json). The uncommitted diff against `HEAD` 08f292a (`git diff --ignore-cr-at-eol`) covers those files plus `docs/increments/INC-001-epic-1-RWB-E1-044.md` and `specify/compliance-validation.md` §4 (the PRE-5 disposition). Checked against `specify/spec.md` (SPEC-RWB-E1-044-001..019), spec gate 4, plan gate 1 (`review/plan-gate-review.md`), `docs/decisions/INC-001-decisions.md` (D-RCV-40, -43, -44, -45, -49), `.github/rules/{pdlc,planning-execution-gates,implementation-execution-gates,traceability-standards}.md` and testing-standards TS-RCV-1..9. I read ACE (`develop` 9f450bbd) without changing it. I also read library facts from the Gradle cache: in Gradle 9.4.1, `gradle-jacoco-9.4.1.jar` `JacocoReportBase` sets `onlyIf("Any of the execution data files exists")`, `executionData(Task...)` adds `mustRunAfter`, and `AntJacocoReport$1$1` passes `getExecutionData().filter(exists)` to Ant. Spring Boot 4.2.0-M2 contains `org.springframework.boot.LazyInitializationBeanFactoryPostProcessor`. I edited nothing except this report.

Human context applied: PRE-1..PRE-4 are approved. PRE-5 was approved by the recovery tech lead on 2026-11-10, during this review: -022..-024 are accepted as carried into tasks, -025 stays in OPEN-019, and the SPEC-015 (a) `spring-boot-testcontainers` deviation is accepted with no `/specify` re-run. I re-read it in plan.md:35, tasks.md:14 and :115, card :147 and :159, and compliance-validation.md:128. Only PRE-6 and PRE-7 are pending, and TASK-00 enforces them.

## Findings

| ID | Severity | Location | Maps to | Issue | Required fix |
|---|---|---|---|---|---|
| REVIEW-RWB-E1-044-037 | Medium | `plan/plan.md:178` (§Coverage, unit gate); `plan/tasks.md:48` (TASK-14 step 2), `:40` (TASK-06 executability rule); `plan/data-model.md` §7 gate table | SPEC-015 (d); TS-RCV-4; `implementation-execution-gates.md:58-60`; REVIEW-026; TASK-06, -14, -16 | The -026 fix moves the unit gate to `test` execution data alone, which is correct. But it sums the five main classes **together with the test tooling `MigrationLint` and `MigrationSqlScanner`** into one figure. Gate 1's required fix (a) asked for the *main-scope* figure. The lint tooling is the bulk of the code and its fixtures test it heavily, so it can lift a low main figure above 80%. That is the masking -026 described, with tooling instead of container data. The risk is real. The -027 rule makes every `ApplicationContextRunner` context lazy and forbids getting the initializer or runner. P-044-04 builds the runner directly. So no `test`-task test runs the `RecoveryFlywayConfig` factory methods `recoveryFlyway`, `recoveryFlywayMigrationInitializer` (with its `ifAvailable` and strategy lambdas) or `recoveryMigrateAndExitRunner`. By estimate, the main METHOD figure is about 14/19 (≈74%), and the gate would still pass. The scope is also a list of class names, not the production directory (`implementation-execution-gates.md:59`: "production-source scope, including untested files … not a narrow selected-file report"). | (1) Make the unit gate the figure for **every class in the main class directory `th/co/scb/ace/demo/recovery/**`** (selected by directory, not by name; the script fails if it finds a main class it did not count) from `test` data alone, at 80% on LINE, INSTRUCTION, BRANCH and METHOD. `MigrationLint`/`MigrationSqlScanner` either get their own unit figure or stay in the combined gate. Do not sum them into the main figure. (2) Add unit tests to TASK-06 that call the factory methods directly on `new RecoveryFlywayConfig()` with stubs. For example: `recoveryFlywayMigrationInitializer(stubFlyway, emptyOrRecordingProvider)` and then run its strategy on a stub `Flyway`; `recoveryMigrateAndExitRunner(...)` with a recording seam, never the default one. With these, the main figure can reach 80% without a container. Or a human records acceptance of the aggregate scope. Update plan §Coverage, §Unit Test Applicability, data-model §7, TASK-14, TASK-16 and the contract `coverage` entry the same way. |
| REVIEW-RWB-E1-044-038 | Low | `plan/tasks.md:48` (TASK-14 step 2), `:47` (TASK-13 verification) | REVIEW-026; SPEC-015 (c)(d); D-RCV-44 | The check that the unit report has no integration data runs only *before* `./gradlew recoveryCoverageReport` (".exec does not exist"). `executionData(tasks.recoveryIntegrationTest)` (a `Task`) adds only `mustRunAfter`, which I checked in the bytecode. But the common form `executionData(tasks.named("recoveryIntegrationTest"))` or `files(provider)` is a `FileCollection` built by the task. It makes the report **depend on** `recoveryIntegrationTest`. Step 2 would then run the container tests and feed their data into the "unit" report without anyone noticing. TASK-13 checks only that `check --dry-run` lists neither task. | TASK-13: add `./gradlew recoveryCoverageReport --dry-run` must not list `recoveryIntegrationTest`, and require the `Task` form (or `mustRunAfter` plus a plain file path) for the extra execution data. TASK-14 step 2: also check after the report that `build/jacoco/recoveryIntegrationTest.exec` is still absent, and save that output with the unit evidence. |
| REVIEW-RWB-E1-044-039 | Low | `plan/plan.md:156`, `:158`; `plan/tasks.md:39` (TASK-05), `:40` (P-044-04); `plan/data-model.md:54`, §4; contract `beans.recoveryMigrateAndExitRunner` | SPEC-005, SPEC-018; REVIEW-028 | The profile-keyed fix meets SPEC-004 (a)–(d), SPEC-005 and D-RCV-45 (see the checks below). It also adds a behaviour the spec does not have. Under `db-migrate-recovery` with the switch not `true`, the runner fails with the new `object=recovery.flyway.migrate-and-exit`. SPEC-018 lists `object` as "version, file, file:line or recoveryFlyway". Failing fast does not contradict SPEC-005, which wants fail fast and no skip. But the new parameter value is a SPEC-018 extension, while the plan says "no SPEC changes", and the human disposition of PRE-5 did not cover it. | Either report this case with `object=recoveryFlyway` (an existing SPEC-018 value, so no deviation), or record the new value as a second accepted spec deviation next to PRE-5 and correct SPEC-018 at the next `/specify`. Keep plan, tasks, data-model and contract the same. |
| REVIEW-RWB-E1-044-040 | Low | `docs/decisions/INC-001-decisions.md:37` | traceability-standards; CLAUDE.md ("new squad decisions start at D-RCV-50") | The register still says "Next free squad number: D-RCV-49", but D-RCV-49 was added at :87 (commit 08f292a). The next decision could reuse the ID. This file is outside the plan artefacts, but this plan's PRE-3/PRE-4 rest on that decision. | Change :37 to "D-RCV-50" (CRLF/LF as the file has it), or hand it to Context Updater. |

## Gate 1 findings: verification

| Gate 1 finding | Result |
|---|---|
| -026 (Medium) | **Partly fixed.** Integration data no longer counts in the unit gate. JaCoCo filters out missing execution-data files, as confirmed from the Gradle 9.4.1 cache, so step 2 can run as written. The summing script is stdlib `python3 -I` and is saved with the evidence. There is no shared-file edit beyond D-RCV-49. Still open: main + tooling are summed into one figure, and the scope is selected by name (see -037). The check that integration data stays out holds only before the report runs (see -038). |
| -027 (Medium) | **Fixed.** `withInitializer(ctx -> ctx.addBeanFactoryPostProcessor(new LazyInitializationBeanFactoryPostProcessor()))`: the class exists in Boot 4.2.0-M2. It runs after `ConfigurationClassPostProcessor` has registered the `@Bean` definitions, and it makes `FlywayMigrationInitializer` and the runner (both `InitializingBean`, not `SmartInitializingSingleton`) lazy. Presence is checked only through `containsBeanDefinition`. The H2 case has no initializer and no runner. P-044-04 builds the runner directly with a recording seam. No `test`-task path reaches `System.exit`, and TASK-15 adds a grep. P-044-03 can now run. The cost to unit coverage is covered in -037. |
| -028 | **Fixed.** `recoveryFlyway ⇔ PG ∧ (DBMR ∨ (FE ∧ ¬DBM))`, initializer ⇔ `PG ∧ FE ∧ ¬DBM`, runner ⇔ `DBMR`. This is the same in data-model §3, TASK-03, -05, plan §Bean design and the contract `activationRule`/`beans`. Under `db-migrate` without `db-migrate-recovery`, none of the three exists, whatever `FE`/`MAE` say (D-RCV-45, SPEC-004 (d)). The new P-044-03 row covers the stray switch. SPEC-004 (a) H2 skip, (b) local start and (c) `scb-aks` are unchanged. SPEC-005 is kept: the runner does not depend on the bean, it fails fast with `object=recoveryFlyway` when the bean is missing or the URL is not PostgreSQL, and the switch is set only in the profile file. For the extra switch check, see -039. |
| -029 | **Fixed.** Sources: `RecoveryFlywayConfig` first, test configuration second. Bean-definition order is the control, and `preInstantiateSingletons` follows that order. A test override of `recoveryFlyway` keeps the name position. `WebApplicationType.NONE` is set on every `SpringApplication`. |
| -030 | **Fixed.** Docker daemon stopped, no `docker.host`/`tc.host`, the Testcontainers error message recorded, plus a static grep. |
| -031 | **Fixed.** The substitution is stated in TASK-12 and scenarios T-044-12. TASK-01 re-checks `AppConfig` :176-219. |
| -032 | **Fixed and closed.** Recorded under PRE-5 and accepted on 2026-11-10 (compliance-validation.md:128). |
| -033 | **Fixed.** `migrateOrReport(Flyway, String jdbcUrl)` is the single reporting path for the initializer, the runner and `RecoveryFlywayIT`. Only `currentSchema` is parsed, and the parameter is left out when the URL has none. T-044-03 `schema=rwb_missing` comes from the test URL. |
| -034 | **No change needed, confirmed.** `requirement/Traceability_Matrix.md`: 427 CRLF lines out of 427 both at `HEAD` and in the working tree. 5720155 (426 → 427 CR) changed 3 lines (`git diff --stat` and `--ignore-cr-at-eol` agree). |
| -035 | **Fixed.** Card stage line :109, "Output run", "Review findings". 164/164 CRLF lines kept. |
| -036 | **Fixed.** `rule=` is used everywhere (plan :164, TASK-07, data-model §4). `OVERLAY` and `IS NOT DISTINCT FROM` fixtures are added and `POSITION` is dropped. The fixture-header rule is the file's own key. HV-1 points at `implement/unit-tests/backend/`. No stale reference is left (grep for `MAE ∨`, `getSchema()`, `reason=`, `DOCKER_HOST`, `implement/backend/`). |

## Checks with no finding

| Check | Result |
|---|---|
| Cross-file consistency | Activation, runner behaviour, report input and both coverage gates read the same in plan.md, tasks.md, data-model.md, scenarios.md and the contract (one exception: -039's object value is consistent everywhere but not in the spec). The contract JSON parses. |
| `BLOCKED_BY` DAG | Re-parsed: 01←00; 02←01; 03←01; 04←03; 05←04; 06←05; 07←01; 08←07; 09←01; 10←02,03; 11←03,04,09,10; 12←05,10; 13←02; 14←06,08,11,12,13; 15,16←14; 17←15,16. Acyclic. Matches `tasks.md:65`. Every build task depends on TASK-00. |
| SPEC → TASK | 19/19 (`tasks.md:69-89`). 22/22 coverage rows COVERED. X1–X12 mapped. |
| `## Pre-submit checks` | Present (`tasks.md:99-117`). Values match the plan, including PRE-1..PRE-5 APPROVED and PRE-6/-7 PENDING. |
| Preconditions | PRE-1..PRE-5 have a decision and a date. PRE-6/-7 are pending and TASK-00 enforces them. The re-run rules (PRE-3 change, a spec change under PRE-5) are kept. |
| Shared-file discipline | Only `backend/build.gradle.kts` among shared files, plus the new profile yaml (D-RCV-49). No new shared-file edit came from the -026/-027 fixes. |
| Line endings | Plan files LF (unchanged), card CRLF 164/164, compliance-validation.md LF (as at `HEAD`), matrix CRLF 427/427. |
| Security, PII, secrets | No credential, token, connection string with host, or customer data. Fixtures are synthetic. The report never reads host, user or password. Auth, audit, KYC/AML, consent and maker-checker are N/A (no endpoint, no business data). |
| UI / frontend | `UI In Scope: NO`, frontend `NOT_APPLICABLE` with SPEC-017 evidence and `N/A` values. No screen mapping needed. |

## Required checks summary

| Check | Result |
|---|---|
| Authentication / authorization | N/A (no endpoint); migration role → OPEN-019 / HV-2 |
| Customer / account data protection | PASS |
| Audit logging | N/A |
| KYC/AML/suitability/consent/approval | N/A |
| Frontend integration versioning / error contract | N/A (`NO_API_CHANGE`, UI NO); MSG-P3-016 ID + parameters (-039) |
| Secrets and environment configuration | PASS |
| Plan requirement coverage | 22/22 rows, 19/19 SPEC |
| Unit-test gates planned | FAIL (-037: main figure not gated on its own; -038 guard) |
| Executability | P-044-03 can run (-027 fixed); unit gate can run (JaCoCo missing-file filter confirmed) |
| Traceability | PASS, with -040 (decision register counter) |
| Approval preconditions | PRE-1..PRE-5 APPROVED; PRE-6, PRE-7 PENDING (TASK-00) |

## Gate result

```text
REVIEW_STATUS: FAIL
REVIEW_TYPE: PLAN_GATE_REVIEW
RUN_ID: INC-001-epic-1-RWB-E1-044
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 3]
REVIEW_BLOCKING: YES [REASON: Medium REVIEW-RWB-E1-044-037 (unit gate sums main classes with lint tooling, selected by name; main-scope unit coverage not gated alone, and the lazy-context design leaves RecoveryFlywayConfig factory methods unexecuted in `test`)]
REVIEW_GATE_WARNING: n/a (Medium finding present; handoff stops)
NEXT_STEP: Implementation Planner remediates -037 (or a human records explicit acceptance), fixes or a human accepts Low -038..-040, then re-runs the plan gate (round 3). Plan approval then needs PRE-6 (FDA) and PRE-7 (FDE). This review does not start Implementation Builder.
```
