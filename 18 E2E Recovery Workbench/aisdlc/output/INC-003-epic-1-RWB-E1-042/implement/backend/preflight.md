# TASK-00 pre-flight on the merged base (read only)

Run: `INC-003-epic-1-RWB-E1-042` · Worktree `rwb-wt/RWB-E1-042` · Branch
`feature/RWB-E1-042-parameter-catalog` cut from `develop-recovery` at `7bee04d`.

| # | Check | Result |
|---|---|---|
| 1 | The worktree carries the RWB-TE-001 and RWB-E1-044 merges | `7bee04d AISDLC: record the RWB-E1-044 merge SHA`, `b1d7424 RWB-E1-044: Database migrations versioned with parameterized schema names`, `e566360 AISDLC-HARDENING: stabilise the platform e2e after sign-in`. RWB-TE-001 is below them (`develop-recovery` history). |
| 2 | The `[TE-001]` homes exist | `access/api/ApiError.java`, `access/api/ApiProblemException.java`, `access/internal/ApiExceptionHandler.java`, `access/internal/ProblemFactory.java`, `casewf/migration/RecoveryFlywayConfig.java` — all present. `recovery/platform`, `recovery/rules`, `recovery/workflow`, `recovery/documents` — absent (`Test-Path` false for all four). |
| 3 | `RecoveryMigrationLintTest` is the identifier-only, quote-aware version | Yes: `architecture/RecoveryMigrationLintTest` drives `architecture/migration/**`, `MigrationLexer` + `LiteralSchemaRule` (`identifierText()`, `isAllowedQualifier`). T-044-21 in place. |
| 4 | `ApiProblemException#error()` call sites | Exactly two, both in `access/internal/ApiExceptionHandler.problem` (the `log.warn` and the `problems.problem` line). No other caller in `backend/src`. |
| 5 | Magic-number baseline re-derived from the merged code | `implement/backend/magic-number-baseline-recheck.csv` (4 HTTP statuses in `ApiError`, `DroolsRuleEngine` 16 / 0.75f, `PdpaPayloadCodec` 12 / 128 / 16 / 24 / 32, `PlatformSmokeWorkflow` 5 / 3, `WorkflowIds` "rwb-recovery" / "rwb-platform"). Derived with `MagicNumberScanner` and confirmed by `RwbMagicNumberCheckTest#theRealMainTreePassesTheReviewedBaseline`. |
| 6 | `classDirectories` include of both JaCoCo tasks | Case 1: the merged filter takes only `architecture/boundary/**` (TE-001) and `architecture/migration/**` (E1-044). `architecture/parameters/**` was **not** taken in, so TASK-21 adds `parameterToolingClasses` to **both** tasks. |
| 7 | Coverage baseline before any change | `./gradlew test recoveryCoverageReport`: BUNDLE LINE 1333/1406 (0.948), INSTRUCTION 7091/7523 (0.942), BRANCH 630/732 (0.861), METHOD 339/346 (0.980). XML saved at `implement/backend/coverage/baseline-recoveryCoverageReport.xml`. |
| 8 | `./gradlew check --dry-run` baseline | `:compileJava :processResources :classes :compileTestJava :processTestResources :testClasses :test :recoveryCoverageReport :check` — neither `recoveryCoverageVerification` nor a tooling gate, as D-RCV-40 expects. Saved at `implement/backend/check-dryrun-baseline.txt`. |
| 9 | Flyway configuration | `RecoveryFlywayConfig`: history table `flyway_schema_history_recovery`, placeholder `recoverySchema` = `rwb.schema`, `cleanDisabled(true)`, `baselineOnMigrate(true)`, `baselineVersion("0")`, `outOfOrder(false)`, `validateOnMigrate(true)`. The migration folder held `README.md` and no `.sql` file. |

Consequences for the plan: TASK-21 applies case 1. The first migration in the folder is `V0001` in this
branch (D-RUN-07: the orchestrator assigns the merge number).
