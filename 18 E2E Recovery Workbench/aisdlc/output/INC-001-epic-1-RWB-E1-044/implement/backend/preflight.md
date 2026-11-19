# TASK-00 pre-flight (RWB-TE-001-merged base)

Worktree: `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-E1-044`
Branch: `feature/RWB-E1-044-db-migrations`, base `develop-recovery`.

## (1) Base contains the RWB-TE-001 merge

```text
$ git log --oneline -5
f36991a AISDLC: record the RWB-TE-001 merge SHA
dc2d25b RWB-TE-001: Recovery module folder and boundary test
d4704d5 AISDLC: plan-phase evidence checkpoint before the first merge
55f1ed4 RWB-TE-001: code gate fixes for the published surface tests (CODE-005, CODE-006)
90550d3 RWB-TE-001: review fix round 1, green (Thai text, external sub-package, lint bypass, dead code)
```

Merge commit of RWB-TE-001: `dc2d25b` (the SHA the brief names). `f36991a` records it. Both are ancestors of
`HEAD`; the worktree was created from `develop-recovery` at `f36991a`.

## (2) `[TE-001]` main paths exist, the old ones are gone

Present:

- `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/migration/RecoveryFlywayConfig.java`
- `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/migration/RecoveryMigrationProperties.java`

Absent: `platform/internal/RecoveryProperties.java` and the four old packages
(`backend/src/main/java/th/co/scb/ace/demo/recovery/platform|rules|workflow|documents`) - the recovery tree
holds the module map packages (`access`, `agent`, `asset`, `casewf`, `comms`, `dataengine`, `debtsale`,
`decision`, `deviation`, `dochub`, `guarantee`, `integration`, `litigation`, `partner`, `payments`,
`reporting`, `treatment`, `valuation`, `writeoff`).

## (3) Registration case: SPEC-002 case 1

`RecoveryFlywayConfig` carries `@EnableConfigurationProperties(RecoveryMigrationProperties.class)` together
with `@ConditionalOnProperty(name = "rwb.flyway.enabled", ...)` (lines 22-25 of the merged file), and no
unconditional registration class exists in `casewf.migration`. **Case 1 applies**: TASK-08 moves the
registration to the new unconditional `MigrationPropertiesConfig`.

## (4) `[TE-001] T/casewf/migration/RecoveryFlywayConfigTest.java`

- `bindsSchemaAndFlywayFromApplicationYaml` uses `ApplicationYamlEnvironment.runner().withUserConfiguration(
  PropertiesRegistration.class)`. `PropertiesRegistration` is a nested `@Configuration` in the test that
  registers `RecoveryMigrationProperties` itself. It creates **no** `DataSource` and **no** `Flyway` bean.
- The other four methods call `new RecoveryFlywayConfig().recoveryFlyway(properties, mock(DataSource.class),
  dataSourceProperties())` directly, so they never start a context and never call `migrate`.
- Tests in the merged tree that bind the record or build `recoveryFlyway`: `RecoveryFlywayConfigTest`
  (all five methods), `ModulithTest` and `RecoveryBoundaryTest` (context-free, main classes only).
- Allowed change (2) applies: `MigrationPropertiesConfig` is added to that one method's user configuration.
  No assertion changes. Change (1) does not apply: `application.yaml` line 74 binds the literal `recovery`.

## (5) Coverage-tooling case: SPEC-014 case 1

`backend/build.gradle.kts` `boundaryToolingClasses` includes only
`th/co/scb/ace/demo/recovery/architecture/boundary/**` (lines 136-141). **Case 1 applies**: TASK-13 adds the
`architecture/migration/**` include to both JaCoCo tasks. `sourceDirectories` already includes
`sourceSets.test.get().java.srcDirs` (lines 148, 161), so TASK-13 adds no source-directory edit.

## (6) Coverage baseline before any E1-044 change

Command (from `backend/`, `JAVA_TOOL_OPTIONS` per RUN-BRIEF, `GRADLE_OPTS=-Xmx512m`):

```text
./gradlew test recoveryCoverageReport --console=plain
BUILD SUCCESSFUL in 6m 53s
```

Saved: `implement/backend/coverage/baseline-recoveryCoverageReport.xml`,
`implement/backend/coverage/baseline-counters.txt`, `implement/baseline-gradle.log`.

BUNDLE counters (all four above 0.80):

| Counter | Missed | Covered | Ratio |
|---|---|---|---|
| LINE | 18 | 692 | 0.9746 |
| INSTRUCTION | 101 | 3656 | 0.9731 |
| BRANCH | 12 | 244 | 0.9531 |
| METHOD | 4 | 187 | 0.9791 |

Measured packages include `th/co/scb/ace/demo/recovery/casewf/migration` and
`th/co/scb/ace/demo/recovery/architecture/boundary`.

## (7) Flyway 12.4.0 API confirmed with `javap`

`implement/backend/javap-flyway.txt` records:

- `Flyway.migrate() : MigrateResult` (throws `FlywayException`),
- `Flyway.validateWithResult() : ValidateResult`,
- `ValidateResult.invalidMigrations : List<ValidateOutput>` and `ValidateOutput.version : String`,
- `Flyway.info() : MigrationInfoService` with `MigrationInfo[] pending()` and
  `MigrationInfo.getVersion() : MigrationVersion`,
- `org.flywaydb.core.api.exception.FlywayValidateException extends FlywayException`.

No mismatch with RWB-TE-001 v4 or plan v7. Nothing in TASK-00 required a stop-and-report.

## (8) `check --dry-run` baseline

`implement/backend/check-dryrun-baseline.txt`. The task graph shows `recoveryCoverageReport` only as the
`test` finalizer and `recoveryCoverageVerification` outside `check`, as the plan expects.
