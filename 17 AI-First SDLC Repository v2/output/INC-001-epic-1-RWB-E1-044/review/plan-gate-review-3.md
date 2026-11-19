---
title: "Plan gate review 3 — RWB-E1-044"
run_id: "INC-001-epic-1-RWB-E1-044"
story: "RWB-E1-044"
jira: "TB0001-1205"
review_type: "PLAN_GATE_REVIEW (gate 3)"
reviewer: "Compliance Reviewer (subagent of Implementation Planner)"
date: "2026-11-10"
---

# Plan gate review 3 — RWB-E1-044

Scope: the revised `output/INC-001-epic-1-RWB-E1-044/plan/` (plan.md, tasks.md, data-model.md, tests/scenarios.md, contracts/backend-apis.json, contracts/frontend-integrations.json), with the gate 2 fixes listed in `plan.md` §"Plan gate 2 remediation (2026-11-10)". The uncommitted diff against `HEAD` 08f292a (`git diff --ignore-cr-at-eol`) covers those files plus `docs/increments/INC-001-epic-1-RWB-E1-044.md`, `docs/decisions/INC-001-decisions.md` and `specify/compliance-validation.md` §4. I checked it against `specify/spec.md` (SPEC-RWB-E1-044-001..019), plan gates 1 and 2 (`review/plan-gate-review.md`, `review/plan-gate-review-2.md`), `docs/decisions/INC-001-decisions.md`, `docs/open-items.md` and `.github/rules/{pdlc,implementation-execution-gates,traceability-standards}.md`. I read ACE (`develop` 9f450bbd, no `recovery` package yet) without changing it.

Library facts I read from the Gradle cache:
- Gradle 9.4.1 `gradle-jacoco-9.4.1.jar`: `JacocoReportBase.executionData(Task...)` takes the task's `JacocoTaskExtension`, then calls `executionData(new JacocoReportBase$2(...))` and `mustRunAfter(task)`. `JacocoReportBase$2` is a plain `Callable<File>` that returns `extension.getDestinationFile()`. It has no build dependency, so the Task overload adds ordering only. The REVIEW-038 claim holds.
- Flyway 12.11.0: `FluentConfiguration.load()` is `new Flyway(this)`. The constructor copies the configuration, loads callbacks, builds `FlywayExecutor`, sets logging and checks the license. It calls nothing on the `DataSource`, so `recoveryFlyway(stubDataSource)` in P-044-07 opens no connection. The plan's "if `load()` opens a connection" fallback will not be needed.

I edited nothing except this report.

Settled by humans, not re-opened: PRE-1..PRE-5 are approved. PRE-5 (2026-11-10) accepted -022..-024, kept -025 in OPEN-019 and accepted the SPEC-015 (a) deviation with no `/specify` re-run. PRE-6 and PRE-7 are pending, and TASK-00 enforces them.

## Findings

| ID | Severity | Location | Maps to | Issue | Required fix |
|---|---|---|---|---|---|
| REVIEW-RWB-E1-044-041 | Low | `plan/plan.md:189` (§Coverage, unit gate); `plan/tasks.md:48` (TASK-14 step 2); `plan/data-model.md` §7 unit row | REVIEW-037 required fix (1); `implementation-execution-gates.md` (production-source scope, including untested files); TASK-14, -16 | The script now lists the class files under `build/classes/java/main/th/co/scb/ace/demo/recovery/` and maps each one to its XML `<class name=…>`. The plan does not say what happens when a listed class file has **no** XML entry. Gate 2 asked for "the script fails if it finds a main class it did not count". As written, an unmatched class could be skipped without anyone noticing. That can happen if the bundle's main filter differs from the directory, which is possible in Case A because RWB-TE-001 owns that filter. A plain "fail on any unmatched file" rule has the opposite problem: it would fail on classes JaCoCo leaves out because they have no code. One example is `package-info.class`, which RWB-TE-001 adds in Case A (TASK-01 uses it to detect Case A). | Add one sentence to plan §Coverage, TASK-14 step 2 and data-model §7: the script fails if a listed class file has no XML `<class>` entry, unless the class has no code (for example `package-info`, or an interface with no method bodies). The script lists those classes by name in its output, which is saved with the evidence. |
| REVIEW-RWB-E1-044-042 | Low | `plan/tasks.md:14` (status paragraph), `:116` (Pre-submit row "Plan gate 1 findings"); `docs/increments/INC-001-epic-1-RWB-E1-044.md:147` ("Plan and tasks" row) | traceability-standards; planning `## Pre-submit checks` | The gate 2 remediation is recorded in `plan.md:72-81`, in `plan.md:286` (status summary) and in the card's "Compliance review" row. Three places still say only "Plan gate 1 findings -026..-036 remediated": the status paragraph at `tasks.md:14`, the Pre-submit checks (no gate 2 row) and the card's "Plan and tasks" row. A reader of tasks.md cannot see that -037..-040 were fixed. | Add "plan gate 2 findings -037..-040 remediated 2026-11-10 (`plan.md` §Plan gate 2 remediation)" to `tasks.md:14`, a Pre-submit row for gate 2, and the same text in card :147. Keep the card's CRLF line endings. |

## Gate 1 and gate 2 findings: verification

| Finding | Result |
|---|---|
| -037 (Medium) | **Fixed** (one script detail is in -041). (a) Scope: the unit gate is now the main class directory `build/classes/java/main/th/co/scb/ace/demo/recovery/**`, selected by directory, from `test` execution data alone. It blocks at 80% on LINE, INSTRUCTION, BRANCH and METHOD (plan :189, TASK-14 step 2, data-model §7, contract `coverage`, TASK-16 "Backend unit" row, §Unit Test Applicability :208). `MigrationLint`/`MigrationSqlScanner` are printed as a separate information figure and are not added to the main figure. They stay gated by the combined gate. No integration data and no tooling substitution in the unit figure. (b) Reachability: P-044-07 (TASK-06 :40, scenarios) calls `recoveryFlyway`, `recoveryFlywayMigrationInitializer` (core present and absent, then `afterPropertiesSet()`, which runs the strategy lambda, `migrateOrReport` and the report-and-rethrow path) and `recoveryMigrateAndExitRunner` directly. P-044-04 covers every runner branch, including the switch check. P-044-03 runs `RecoveryFlywayCondition` and `RecoveryLocalStartCondition` over every truth-table row (conditions are evaluated even in lazy contexts). P-044-05 covers `RecoveryMigrationReport`. The only main code no `test`-task test can run is the default `RecoveryMigrationExit` (`System.exit(SpringApplication.exit(context, () -> code))` and the supplier that picks it). That is about 2–3 synthetic lambda methods and 1–2 lines out of about 20 methods, so the main figure can reasonably reach 80% without a container (estimate, not measured). Note for the Builder: TASK-04's factory signature `(Flyway, ObjectProvider)` does not say where the strategy gets `spring.datasource.url`, for example an `Environment` injected into `RecoveryFlywayConfig`. P-044-07 has to supply it the same way. This is not a finding. |
| -038 (Low) | **Fixed.** TASK-13 :47 requires `executionData(tasks["recoveryIntegrationTest"])`, the eager `Task` overload. It forbids `tasks.named(...)`, providers and `files(provider)`, and checks that `./gradlew recoveryCoverageReport --dry-run` does not list `recoveryIntegrationTest`. The cache confirms that the overload adds a `Callable<File>` plus `mustRunAfter` and no dependency, so the dry-run check is correct and will pass. TASK-14 step 2 runs `ls build/jacoco/` before and after the report, and both outputs are saved. Together with JaCoCo's missing-file filter (confirmed in gate 2) this is enough. Integration data cannot get into the unit report by a task dependency or by being present beforehand. |
| -039 (Low) | **Fixed.** The runner's switch check now reports `object=recoveryFlyway`, with the reason naming the switch (plan :80, :167, :169; TASK-05, TASK-06; data-model §4 and the "switch overridden" row; contract `beans.recoveryMigrateAndExitRunner`; scenarios P-044-04). A grep of `plan/` for `object=` finds only `<version>`, `recoveryFlyway`, `<file>[:<line>]`, and the comparator's `<table.column>`/schema object, which SPEC-012/-018 already use (spec :200). No `object=recovery.flyway.migrate-and-exit` is left. |
| -040 (Low) | **Fixed.** `docs/decisions/INC-001-decisions.md:37` now says "Next free squad number: D-RCV-50". D-RCV-49 is at :87, and no D-RCV-50 entry exists. The file has LF line endings, as at `HEAD` (0 CRLF). |
| -026, -027 (Medium, gate 1) | **Stay closed.** The -026 rest (main + tooling summed, selected by name) is closed by -037. The -027 lazy-context rule is unchanged. P-044-07 adds coverage but never calls the default exit seam: it uses a recording seam and the TASK-15 grep remains. |
| -028..-036 (Low, gate 1) | **Stay closed.** Activation (`recoveryFlyway ⇔ PG ∧ (DBMR ∨ (FE ∧ ¬DBM))`, initializer ⇔ `PG ∧ FE ∧ ¬DBM`, runner ⇔ `DBMR`) is the same in data-model §3, plan §Bean design, TASK-03/-05 and the contract `activationRule`/`beans`. Source order and `WebApplicationType.NONE` (-029), the Docker-stopped evidence (-030), the substitution (-031), PRE-5 (-032), `migrateOrReport` with URL-only `currentSchema` (-033), the matrix CRLF (-034), the card (-035) and `rule=`/fixtures (-036) are all unchanged. |

## Checks with no finding

| Check | Result |
|---|---|
| Cross-file consistency | The unit gate scope, execution-data form, activation, runner fail-fast and `object` values read the same in plan.md, tasks.md, data-model.md, scenarios.md and the contract. The exception is the stale status lines in -042. Both contract JSON files parse. |
| `BLOCKED_BY` DAG | 01←00; 02←01; 03←01; 04←03; 05←04; 06←05; 07←01; 08←07; 09←01; 10←02,03; 11←03,04,09,10; 12←05,10; 13←02; 14←06,08,11,12,13; 15,16←14; 17←15,16. Acyclic. Matches `tasks.md:65` and the drawing. Every build task depends on TASK-00. |
| SPEC → TASK | 19/19 (`tasks.md:69-89`). 22/22 coverage rows COVERED. X1–X12 mapped. P-044-07 is traced to SPEC-001, -004 (b), -005, -018. |
| `## Pre-submit checks` | Present (`tasks.md:99-117`). The values match the plan except the missing gate 2 row (-042). |
| Preconditions | PRE-1..PRE-5 have a decision and a date (plan :31-35, tasks :14, compliance-validation.md §4, card). PRE-6/-7 are PENDING and TASK-00 enforces them. The re-run rules are kept. |
| Shared-file discipline | The gate 2 fixes add no shared-file edit. Only `backend/build.gradle.kts` (TASK-02, -13) and the new profile yaml, both covered by D-RCV-49 / OPEN-030. `AppConfig.java`, `application.yaml`, `SampleModuleConfig.java`, security and CI files stay unedited (TASK-15). |
| Line endings | Card CRLF 164/164 (as at `HEAD`). `Traceability_Matrix.md` CRLF 427/427. Decisions file and plan files LF, as at `HEAD`. |
| Security, PII, secrets | No credential, token, connection string with a host, or customer data in the plan files. The grep finds only the word "token" for the SQL tokenizer and the guardrail rows. Fixtures are synthetic. Auth, audit, KYC/AML, consent and maker-checker are N/A (no endpoint, no business data). |
| UI / frontend | `UI In Scope: NO`. Frontend is `NOT_APPLICABLE` with SPEC-017 evidence and `N/A` values. No screen mapping is needed. |

## Required checks summary

| Check | Result |
|---|---|
| Authentication / authorization | N/A (no endpoint); migration role → OPEN-019 / HV-2 |
| Customer / account data protection | PASS |
| Audit logging | N/A |
| KYC/AML/suitability/consent/approval | N/A |
| Frontend integration versioning / error contract | N/A (`NO_API_CHANGE`, UI NO); MSG-P3-016 uses SPEC-018 parameters only |
| Secrets and environment configuration | PASS |
| Plan requirement coverage | 22/22 rows, 19/19 SPEC |
| Unit-test gates planned | PASS, with -041 (script must fail on a main class it did not count): main-scope unit gate from `test` data alone, 80% on four metrics; combined gate separate; frontend `NOT_APPLICABLE` |
| Executability | Task overload confirmed with no dependency; `load()` opens no connection; P-044-07 can run without a container |
| Traceability | PASS, with -042 (stale gate status in tasks.md and card) |
| Approval preconditions | PRE-1..PRE-5 APPROVED; PRE-6, PRE-7 PENDING (TASK-00) |

## Gate result

```text
REVIEW_STATUS: FAIL
REVIEW_TYPE: PLAN_GATE_REVIEW
RUN_ID: INC-001-epic-1-RWB-E1-044
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
REVIEW_BLOCKING: NO [REASON: Low-only findings (REVIEW-RWB-E1-044-041, -042); gate 1 and gate 2 findings -026..-040 closed]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
NEXT_STEP: Human disposition of Low -041 and -042 (fix in the plan or accept). Then the recovery tech lead records plan approval (PRE-6, FDA) and task approval (PRE-7, FDE) in the increment card. Implementation Builder starts only when a human runs /implement after TASK-00 passes. This review does not start Implementation Builder.
```
