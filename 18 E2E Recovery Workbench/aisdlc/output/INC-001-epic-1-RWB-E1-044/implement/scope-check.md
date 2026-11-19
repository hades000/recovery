# TASK-19 scope, guardrail and evidence check

Worktree `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-E1-044`,
branch `feature/RWB-E1-044-db-migrations`, base `f36991a` (RWB-TE-001 merged). Diff range
`f36991a..HEAD`: 121 files, 3767 insertions, 96 deletions.

## (1) The diff touches only the files `plan.md` lists

Changed top-level paths: `backend/build.gradle.kts`, `backend/src/**`, `docs/stories/RWB-E1-044/**`,
`infra/postgres/init/**`. Every file is on the plan's "Files added or changed" tables
(CODE-E044-001..031 in `code-map.md`). The one shared file edited is `backend/build.gradle.kts`
(D-RCV-40).

```text
$ git diff --name-only f36991a..HEAD | Select-String "application.*\.yaml|\.gitlab-ci|scripts/dev.ps1|^frontend/|^api/|db/modulemigration/recovery/.*\.sql"
(no output)
```

`application*.yaml`, `.gitlab-ci.yml`, `scripts/dev.ps1`, `frontend/**` and `api/**` are unchanged.

## (2) No new dependency

```text
$ git diff f36991a..HEAD -- backend/build.gradle.kts | Select-String "implementation\(|testImplementation\(|runtimeOnly\(|testRuntimeOnly\("
none
```

The build-file change adds one `migrationToolingClasses` file collection and adds it to
`classDirectories` of both JaCoCo tasks. No dependency block changed; `spring-boot-starter-validation`
and logback-classic were already present (plan "Change scope and surfaces").

## (3) No recovery migration file

```text
$ (Get-ChildItem backend/src/main/resources/db/modulemigration/recovery -Filter *.sql).Count
0
```

Only `README.md` is in the production folder. Every `V<seq>__…` file in the diff is a test fixture
under `backend/src/test/resources/migration-lint/` or `.../flyway-fixtures/` (ASM-E044-014).

## (4) SPEC-017 exclusions not built

```text
$ Select-String -Path <new main/test code> -Pattern "MigrationRunRecorder|admin/jobs|migration-drift-gate|SCR-44|SET ROLE"
(no output)
```

- No `MigrationRunRecorder`, no `GET /admin/jobs?type=MIGRATION`, no SCR-44 display, no `MSG-P4-002`.
- No drift flag, no read-only account, no real-environment comparison.
- No ACE DBA role: the init diff grants `USAGE ON SCHEMA public` and
  `ace_view_owner ... WITH INHERIT FALSE, SET TRUE` only. No table privilege, no `CREATE` on
  `public`, no `ADMIN`, no other membership.
- No `SET ROLE` lint rule (seam OI-E044-J).

## (5) SPEC-016 single decision point and the seam marker

`isAllowedQualifier(MigrationStatement, String)` in `LiteralSchemaRule` is the only qualifier
decision point (4 references: the method, its one call, and two Javadoc links). It returns true only
for `${recoverySchema}`, `information_schema` and `pg_catalog`; there is no `public` exception.
`ForeignKeyOutsideRule` never calls it. The seam-marker fixture `t02-seam-marker-fail` still gives one
`L-LITERAL-SCHEMA` at :2 and its parameterised test is green.

## (6) No personal data, credential or production data

Fixtures use synthetic names (`queue`, `timer`, `t1`, `c1`, `account_id`, `note_x`) and the ACE
table name `public.account`. No customer name, ID number, account number or address appears in code,
fixtures, logs or this evidence. The container tests use synthetic container passwords
(`it-migrator`, `it-recovery`, `it-temporal`). No secret is read from `.env` by any test this story
adds. The `MSG-P3-016` line holds the message ID and two parameters only; T-044-09 asserts no `jdbc`,
`password` or `SELECT` text.

## (7) Unit-test results table

See `implement/unit-tests/report.md`. Backend PASS (226 passed, 0 failed, 0 skipped; INSTRUCTION
0.9399, BRANCH 0.8651, LINE 0.9457, METHOD 0.9768 against 0.80); frontend `NOT_APPLICABLE` with `N/A`
counts and the plan rationale; native report `implement/backend/coverage/recoveryCoverageReport.xml`.

## (8) RWB-TE-001 tests green; only the allowed change

`RecoveryFlywayConfigTest` 5 tests, `ModulithTest` 2, `RecoveryBoundaryTest` 11 - all green in the
226-test run. The diff to `RecoveryFlywayConfigTest` is exactly SPEC-002 change (2): adding
`MigrationPropertiesConfig` to the user configuration of `bindsSchemaAndFlywayFromApplicationYaml`.
No assertion changed, and no other method changed.

```text
-		ApplicationYamlEnvironment.runner().withUserConfiguration(PropertiesRegistration.class).run(context -> {
+		ApplicationYamlEnvironment.runner()
+			.withUserConfiguration(PropertiesRegistration.class, MigrationPropertiesConfig.class)
+			.run(context -> {
```

All eight items are ticked. Scope verdict: PASS.
