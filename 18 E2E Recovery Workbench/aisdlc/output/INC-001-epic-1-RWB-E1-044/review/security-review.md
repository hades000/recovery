---
title: "Security review: RWB-E1-044 database migrations versioned with parameterized schema names"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
gate: Security (pre-merge review of the story diff)
date: 2026-11-18
range: develop-recovery...feature/RWB-E1-044-db-migrations
tip: 1ac16c0
result: PASS WITH FINDINGS (0 Critical, 0 High, 0 Medium, 4 Low, 1 Informational)
reviewer: Security Reviewer subagent, started by the orchestrator
---

# Security review: RWB-E1-044

## 1. Scope and method

Reviewed the whole story diff, 121 files, +3767/−96, commits `ed4f496` to `1ac16c0`
(`ed4f496` tokenizer, `42eb802` rules and corpus, `98e661e` snapshot reader and comparator,
`b3bc5ce` schema pin, `e8581b4` failure mapping, `a9400ed` container proof and D-RUN-14,
`1ac16c0` coverage wiring and docs); tip `1ac16c0`.

Read in full: every new or changed Java file under
`backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/migration/` and
`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/` (including the lexer, all 15
rules, lint, comparator, snapshot reader and the three new test classes), every fixture under
`backend/src/test/resources/flyway-fixtures/` and `backend/src/test/resources/migration-lint/`,
`infra/postgres/init/00-roles-and-databases.sh`, `20-grants.sql.inc`,
`backend/src/main/resources/db/modulemigration/recovery/README.md`, the changed blocks of
`backend/build.gradle.kts`, `docs/stories/RWB-E1-044/story.md` and `plan.md`, and the diff's
`RecoveryFlywayConfigTest.java` change. Read for rules: `aisdlc/RUN-BRIEF.md`, `AGENTS.md`,
`aisdlc/.github/rules/security-quality-standards.md`,
`aisdlc/.github/contexts/backend-standards.md`, the E1-044 spec v14-7, and D-RUN-14 in
`AI-SDLC-BUILD-LOG.md`.

No Gradle, Testcontainers or Docker run was made in this review. Three standalone probe programs
were run against the story's compiled test classes (`backend/build/classes/java/test`) to confirm
behaviour where static reading left doubt; they exercised the real `MigrationLint`,
`MigrationLexer` and rules. The probes live outside the repository and changed no repo file. Only
this file was written. No code, test, plan or shared file was edited. No question was put to the
user.

## 2. Findings summary

| ID | Severity | Area | Headline |
|---|---|---|---|
| SEC-044-01 | Low | Fail-open guard | A missing migration folder makes the production lint pass while checking zero files |
| SEC-044-02 | Low | SQL parsing | `L-LITERAL-SCHEMA`/`L-FK-OUTSIDE` miss a qualifier split before the dot across a newline |
| SEC-044-03 | Low | SQL parsing | `L-GRANT` is bypassed by `GRANT` hidden in `DO`/`EXECUTE` dynamic SQL |
| SEC-044-04 | Low | Failure reporting | A connection-type failure loses the `MSG-P3-016` line and the original cause because `flyway.info()` also throws |
| SEC-044-05 | Informational | Pathological input | Super-linear block-comment scan (200 KB → 46 s) and stack overflow on nested dollar tags |

No Critical, High or Medium finding. Sections 4 and 5 list the checks that found nothing and the
documented residual risks.

## 3. Findings

### SEC-044-01 — The production lint fails open when its folder is absent (Low)

**Files.** `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/MigrationLint.java:28`
(`if (!Files.isDirectory(folder)) { return List.of(); }`) and
`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryMigrationLintTest.java:49`
(`assertThat(MigrationLint.lint(MIGRATIONS)).isEmpty()`).

**Failure case.** `MIGRATIONS` is the relative path
`src/main/resources/db/modulemigration/recovery`. If the folder is renamed or removed, or the test
runs with a different working directory (an IDE run from the repository root, for example),
`Files.isDirectory` is false and the lint returns no findings. `migrationsFollowTheRecoveryRules`
then passes while no migration has been checked, so every D-RCV-28 rule is silently off for the
production folder. The probe `MigrationLint.lint(<non-existent path>)` returned `[]`.

**Impact.** A build-time control disappears without a failed test. The database still refuses
cross-schema reads and writes under D-RUN-14, so this is not a data-exposure path today, but the
naming, header, sequence and grant rules are not enforced by the database.

**Smallest fix.** Throw from `lint` when `!Files.isDirectory(folder)` (for example
`UncheckedIOException("migration folder not found: " + folder, ...)`). The existing
`anEmptyFolderGivesNoFinding` test uses a real `@TempDir`, so it still passes.

### SEC-044-02 — A literal schema qualifier split before the dot is not reported (Low)

**Files.** `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/rule/LiteralSchemaRule.java:54`
(`file.identifierText().lines()` — every pattern is applied line by line) with the patterns at
lines 37–45, and `.../rule/ForeignKeyOutsideRule.java:33-37` (same per-line pattern).

**Failure case.** The probe ran the real lint on a valid fixture containing:

```sql
ALTER TABLE public
.t1 ADD COLUMN c int;
SELECT count(*) FROM public
.account;
```

It returned `[]`. `QUALIFIED` needs `public` and `.` on the same line; `POSITION` needs the
keyword, the qualifier and the dot on the same line. PostgreSQL accepts whitespace (including a
newline) around the dot, so the statement executes. The same bypass works with a `--` comment
between `public` and the dot, and with a split `REFERENCES public` / `.account(id)` (DB refusal
still applies).

**Impact.** AC5 says a literal schema qualifier fails the build, and the lint is the control that
keeps `public`/`ace` references out of recovery migrations. Under D-RUN-14 the migrator holds no
table privilege and no `CREATE` on `public`, so the database refuses the action; this is a lost
defence-in-depth layer and becomes material if the OI-E044-I environment grants are widened.

**Smallest fix.** Apply the two patterns to the whole identifier text (the existing `\s*` already
matches newlines), derive the line from the match offset, and keep the existing
(rule, file, line, name) de-duplication. Add the split fixture to `t21-literal-negatives-fail` and
to `t05-fk-public-fail`.

### SEC-044-03 — `L-GRANT` is bypassed by dynamic SQL in `DO`/`EXECUTE` (Low)

**File.** `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/rule/GrantRule.java:30-40`.
The rule only looks at the first word of a physical line and the first word of a statement.

**Failure case.** A valid fixture with

```sql
DO $$ BEGIN EXECUTE 'GRANT SELECT ON recovery.queue TO PUBLIC'; END $$;
```

returns `[]` from the real lint. A `CREATE FUNCTION ... LANGUAGE plpgsql AS $$ BEGIN EXECUTE
'GRANT SELECT ON recovery.queue TO PUBLIC'; END $$;` fixture also returns `[]`. The `GRANT` is
inside a string, so the code text keeps it but it is not the first word of a line or statement.
At startup this runs as `rwb_migrator`, which owns the recovery tables and can grant on them.

**Impact.** The D-RCV-28/BS-2.5 "no GRANT/REVOKE in a recovery migration" control is bypassable.
The practical exposure is limited locally because only `rwb_migrator` and `recovery_svc` have
`CONNECT` on `ace` and `recovery_svc` already has DML on the recovery tables; in a target
environment with more ACE roles holding `CONNECT`, a grant to `PUBLIC` would widen read access to
recovery data. It requires migration authorship and a reviewer missing the block, so it is not a
direct privilege escalation.

**Smallest fix.** In `GrantRule`, for every statement whose first word is `DO` or `EXECUTE`, read
the same offset range from `codeText()` and fail if it contains `GRANT` or `REVOKE`
(case-insensitive); add both fixtures to `t20-grant-fail`. A `CREATE FUNCTION` body that uses
dynamic SQL is the same class; either extend the check to function bodies or record it with
SEC-044-02 as a lexical-rule limitation.

### SEC-044-04 — A failure with no version can lose the MSG-P3-016 line and mask the cause (Low)

**File.** `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/migration/RecoveryMigrationRunner.java:50-66`;
`flyway.info()` is called at line 62 from inside the `catch (FlywayException failure)` block at
lines 39–43.

**Failure case.** With the database down, the schema missing, or the connection refused,
`migrate()` throws `FlywayException`; the handler calls `failureObject`, whose `flyway.info()` must
also connect and therefore throws a second `FlywayException` before `log.error` at line 40 runs.
The required `MSG-P3-016 schema=recovery object=recoveryFlyway` line is never written, and the
exception that reaches Spring is the `info()` failure, not the original. The unit test
`aConnectionFailureWithNoVersionUsesTheBeanName` mocks `info()` to return an empty service, so the
real path is untested. This is the one row of SPEC-003's `object` table that is unreachable.

**Impact.** Availability and diagnosis, not confidentiality: the context still fails, so the
service does not start. AC8/X6's "the failure is recorded" evidence is lost for exactly the
failure kinds the spec names.

**Smallest fix.** Wrap the `failureObject` call in `try { … } catch (RuntimeException ignored) {
object = FALLBACK_OBJECT; }` and log the original failure; add a unit test where `info()` throws.

### SEC-044-05 — Pathological SQL input makes the lint super-linear and can overflow the stack (Informational)

**File.** `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/MigrationLexer.java:155-165`
and `blockCommentEnd` at lines 274–294; `Files.readString` at line 25 has no size cap; `dollarBody`
at lines 202–212 recurses once per nested body.

**Failure case.** The probe parsed repeated `/*` with no `*/`:

| Input | Time |
|---|---|
| 50 KB | 806 ms |
| 100 KB | 5.26 s |
| 200 KB | 45.8 s |

Each unterminated `/*` restarts a scan to end of file, so a 1 MB file is roughly 20 minutes. A
78 KB file of nested dollar tags (`$t0$ $t1$ … $t4999$ … $t0$`) throws `StackOverflowError` at
about 5,000 levels. `Files.readString` also has no size cap, so a very large `.sql` file is read
whole.

**Impact.** A build-time denial of service on the shared CI. It requires a contributor able to add
a migration file (the same trust as build scripts), and it fails the build rather than bypassing a
rule, so it is informational, not a boundary break.

**Smallest fix.** Cap the file size (for example 256 KB) and report larger files as a finding, cap
dollar-body nesting at a small depth (or make the scan iterative), and make `blockCommentEnd`
remember the first offset with no closing `*/` so repeated openers do not rescan. The size cap
alone still leaves a few seconds at the cap; the memoised scan removes the quadratic term.

## 4. Checks performed

| Check | Result | Evidence |
|---|---|---|
| Secrets, credentials, tokens, connection strings | Clean | No secret added in Java, SQL, YAML, shell, fixtures, README or docs. The only literals are synthetic (`it-migrator`, `it-recovery`, `it-temporal`), the same pattern as the existing `RecoveryDatabaseIT`; `rwb.flyway.password` stays `${RWB_MIGRATOR_PASSWORD:}`; `RecoveryMigrationRunner` logs only schema and version; `.env` is git-ignored (`.gitignore:2`) and `.env.example` is unchanged baseline. |
| PII and production data | Clean | Every fixture uses synthetic names (`queue`, `timer`, `account_key`, `t1`, `t2`); no rows of personal data; the only `public.account` mention is the intentional FK-refusal fixture, never executed as data. |
| File and path handling | One Low (SEC-044-01), one Info (SEC-044-05) | Fixture roots, temp copies and migration paths come from literals; `SchemaSnapshotReader.read` uses `PreparedStatement` parameters, so a schema name is never concatenated; `MigrationLint` lists direct entries only and throws `UncheckedIOException` on an unreadable entry (`RecoveryMigrationLintTest.anUnreadableSqlEntryFailsClosed`); no traversal or TOCTOU path found; the missing-folder case is SEC-044-01, the unbounded read is SEC-044-05. |
| SQL tokenizer: comments, strings, quoted identifiers, dollar quotes | Clean | One quote-aware pass; nesting counted; `E'` backslash escapes and doubled quotes; `$$`/`$tag$` bodies re-tokenized with the body end winning; `${recoverySchema}` is identifier text, not a dollar quote; `;` cuts only at top level; unterminated openers produce L-LEX and scanning resumes, so nothing is hidden. T-044-22 cases N1–N15/P1–P3 and `MigrationLexerTest` cover the adversarial shapes. No catastrophic regex backtracking found in the lint's regexes. |
| Fail-open vs fail-closed | Four Low findings above | Unreadable entries and directories fail closed; a missing folder fails open (SEC-044-01); the line-based literal/FK rules and the first-word grant rule fail open (SEC-044-02, -03); all other rules report on the complete file. |
| Migration execution safety | Clean | No production migration file: `backend/src/main/resources/db/modulemigration/recovery/` still contains only `README.md`; the diff modifies no `db/modulemigration/**/*.sql` and no merged migration; `cleanDisabled(true)`, `validateOnMigrate(true)`, `outOfOrder(false)`, `createSchemas(false)`, `baselineVersion("0")`, `baselineOnMigrate(true)` and `validateMigrationNaming(true)` are all set (`RecoveryFlywayConfig.java:35-47`). No `R__` or `U` file reaches the production path; the fixtures with `TRUNCATE`/`UPDATE` are lint-only text, not Flyway locations. |
| Schema pin in both modes | Clean | `RecoveryMigrationProperties` is `@Validated` with `@NotNull` + `@Pattern(regexp = "recovery")` on `schema` (`:17-22`); `MigrationPropertiesConfig` registers it with no condition (`:10-12`); `MigrationPropertiesConfigTest` proves a wrong or blank schema fails with `rwb.flyway.enabled` true and false, through an environment override, and that direct construction is unaffected. |
| D-RUN-14 rights | Clean (matches the decision) | `20-grants.sql.inc:17-18` grants exactly `USAGE ON SCHEMA public` and `ace_view_owner WITH INHERIT FALSE, SET TRUE`; no table privilege, no `CREATE` on public, no ACE DBA role, no other membership; `00-roles-and-databases.sh` still creates `rwb_migrator` with `LOGIN` only; T-044-17 (a)–(f) checks `USAGE`/no `CREATE`, one membership with `inherit_option = false`, `set_option = true`, `admin_option = false`, no `rolsuper`/`rolcreaterole`/`rolcreatedb`/`rolbypassrls`, zero `public` table privileges, and SQLSTATE `42501` for both a direct read and the FK probe. |
| New dependencies / build-script injection | Clean | `backend/build.gradle.kts` changes only the `migrationToolingClasses` file set and its two task references; no dependency, plugin, repository, `exec` or external command is added; no `.gitlab-ci.yml` or Dockerfile change. |
| Tests | Clean | No `@Disabled`, `@Ignore`, `assumeTrue` or silent skip in the diff; the replaced inline lint test is superseded by the fixture corpus with complete-list assertions; `RecoveryFlywayConfigTest` only adds `MigrationPropertiesConfig` to the context, no assertion changed. |
| Logs | Clean | The only added log line is `MSG-P3-016 schema={} object={}`; the test asserts it contains no `jdbc`, `password` or `SELECT`; the rethrown Flyway exception can carry DDL and reference-data SQL, never personal data (SPEC-003, accepted). |
| API/authorization | Not applicable | No endpoint, controller, route or security configuration changed; the spec records NO_API_CHANGE. |
| Scope and traceability | Clean | The diff carries the story and plan under `docs/stories/RWB-E1-044/`; the production migration count is zero, as D-RCV-28 and story v7 §13 require; no frontend file. |

## 5. Accepted risks and notes

| ID | Risk | Status |
|---|---|---|
| R-1 | With `SET TRUE`, a recovery migration can `SET ROLE ace_view_owner` and read ACE tables (directly or through a definer view it creates), bypassing AGENTS §3.12. No lint rule shipped here refuses `SET ROLE`. | Documented in SPEC-017 and OI-E044-J; accepted by D-RUN-14 pending the recovery tech lead's confirmation. Inherent impact Medium; not a new finding against this diff. Recommended: add the `SET ROLE` lint rule (outside the RWB-E1-069 view statements) as part of OI-E044-J, and keep the code review control until then. |
| R-2 | Spring logs the rethrown Flyway exception, which can include the failing SQL statement. | Accepted by SPEC-003. Recovery migrations hold DDL and reference data only; no personal data; audit A-07 masking is RWB-TE-011's. |
| R-3 | The drift comparator's only container test reads both databases as the container superuser; the read-only drift account is not exercised. | Out of scope by D-RCV-05 (parked); the reader takes any `Connection`, so a later story can pass a read-only one. |
| R-4 | BS-2.5 v2 still says the migration account holds the ACE DBA role for the release window. | Superseded for this story by D-RUN-14 and DG-L13; the code and test implement the narrower rights. The standard text should be corrected by its owner; no code change requested here. |
| R-5 | `00-roles-and-databases.sh` interpolates passwords into SQL. | Pre-existing baseline, unchanged by this diff (comments only), local-only script with synthetic values. Not a finding for this story. |

## 6. Result

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 0 | — |
| Low | 4 | SEC-044-01, -02, -03, -04 |
| Informational | 1 | SEC-044-05 |

The story diff has no security blocker. The four Low findings are in
test-scope lint tooling and in the failure-reporting path, not in a production request path; none
exposes a secret, personal data, ACE data or a production credential, and none weakens a database
grant. The database boundary required by D-RUN-14 is implemented exactly as decided and is proven
by T-044-17. The open item OI-E044-J (the `SET ROLE` residual) remains the one risk the tech lead
must confirm; it is recorded by the spec, not introduced here.

SECURITY_REVIEW: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4] [INFO: 1]

## Fix round 1 verification (`c253b3c`)

Re-checked the fix commit against prior tip `1ac16c0` (24 files, +370/−135). Read every
changed file; ran `RecoveryMigrationRunnerTest`, `RecoveryMigrationLintTest`,
`MigrationLexerTest`, `SchemaComparatorTest` and `MigrationPropertiesConfigTest` under
`./gradlew test` (9, 60, 19, 7 and 6 tests; 0 failures, 0 skips) plus standalone probes for the
edge cases below. Only this section was appended.

| Item | Status | Evidence and residual |
|---|---|---|
| SEC-044-01 Low — missing folder | **CLOSED** | `MigrationLint.lint` no longer returns `List.of()`; `Files.list` on a missing path throws `UncheckedIOException`. New `aMissingFolderFailsClosed` passes; probe confirms, and an empty folder still gives `[]`. |
| SEC-044-02 Low — split qualifier | **CLOSED** | `LiteralSchemaRule` and `ForeignKeyOutsideRule` match over the whole identifier text and map the match to a line. New `t21-split-qualifier-fail` (lines 2 and 4) and `t05-fk-split-fail` (L-LITERAL + L-FK line 2) pass; probes of `ALTER TABLE public` / `.t1` and `FROM public -- c` / `.account` find both. |
| SEC-044-03 Low — GRANT in dynamic SQL | **CLOSED** | `GrantRule` also checks `DO`/`EXECUTE` statements for `GRANT`/`REVOKE` in the code text. `t20-grant-fail` lines 5–6 pass; probes of the `DO $$ EXECUTE 'GRANT …' $$` and function forms both give L-GRANT. |
| SEC-044-04 Low — failure masking | **CLOSED** | `failureObject` catches `RuntimeException` and returns `recoveryFlyway`; the original exception is rethrown. `aDetailLookupFailureStillLogsTheFallbackAndRethrows` and the real `aBrokenConnectionStillLogsTheFallbackAndRethrows` (`jdbc:postgresql://127.0.0.1:1/ace`) pass; 9/9 runner tests. |
| SEC-044-05 Info — pathological input | **CLOSED for the reported DoS; two Info residuals** | 262,144-character cap and depth-32 cap both fail with `IllegalArgumentException`; 200 KB of `/*` parses in 18 ms and the 5 s JUnit timeout test passes with 100,000 L-LEX findings; size+1 and depth 40 fail closed. **Residuals (Info, no fail-open):** (a) `parse(Path)` calls `Files.readString` before the cap, so a huge file can still OOM; add a `Files.size` check before the read. (b) The block-comment memo is unsound across nesting contexts: `/* /* */` gives two L-LEX, and `/* unterminated` followed by a dollar body containing `/* balanced */` suppresses a later `public.t` L-LITERAL. Both inputs already fail L-LEX, so no valid file passes; memoise only when no `*/` exists in `[from, limit)`. The binary-search `lineOf` is correct for LF/CRLF and every offset (probe). |
| D-RUN-14 | **CLEAN** | No `infra/` file changed in this commit; `20-grants.sql.inc` still grants only `USAGE ON SCHEMA public` and `ace_view_owner WITH INHERIT FALSE, SET TRUE`, with no table privilege, no ACE DBA and no other membership; T-044-17 is unchanged. |
| Secrets, PII, dependencies | **CLEAN** | New tests use `synthetic-password` and `127.0.0.1:1`; new fixtures are synthetic; no secret, PII, dependency, plugin or build-script change (`build.gradle.kts` is not in the fix commit). |

**Verdict.** All four Low findings are closed and verified. The Info finding is closed for the
reported quadratic/stack-overflow and the 200 KB bound; two Info-only residuals remain
(read-before-size-check and the unsound memo edge on files that already fail L-LEX). Neither
exposes data, a secret or a new fail-open on a valid file.

SECURITY_REVIEW: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0] [INFO: 2]
