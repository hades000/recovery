## What this change does

It adds the test-scope migration-lint tooling (one quote-aware tokenizer, a parsed-file model, 15 rules and a fixture corpus), a schema-snapshot reader and pure drift comparator, a `rwb.schema=recovery` pin with an unconditional properties class, a `RecoveryMigrationRunner` that reports a failed migrate as `MSG-P3-016`, the D-RUN-14 local migrator rights, container proof of the Flyway behaviour, coverage wiring and the migration-folder README. It ships no production migration and adds no endpoint, screen or dependency.

Reviewed the full diff at tip `1ac16c0`. Load assumed: one developer build and CI scanning a small migration folder; the container test runs Flyway once per build. I ran `./gradlew test` (all green; 55 lint tests, 15 lexer tests, 6 comparator tests, 6 runner tests, 6 pin tests), `recoveryIntegrationTest` for `RecoveryMigrationIT` (11/11 green) and `RecoveryDatabaseIT` (green), and `recoveryCoverageVerification` (PASS; 94.6% line, 86.5% branch).

## Must fix

1. **A database outage at startup logs no `MSG-P3-016` line** (`backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/migration/RecoveryMigrationRunner.java:L39-67`; test `RecoveryMigrationRunnerTest.java:L102-115`)
   - **What this is:** When `flyway.migrate()` fails, the runner asks Flyway again for a version to put in `MSG-P3-016 schema=recovery object=<version>`, logs one ERROR line, then rethrows.
   - **Problem:** On a connection failure or a missing schema, `flyway.info()` needs the same broken database and throws, so the ERROR line is never written and the second exception replaces the original. I confirmed with Flyway 12.4.0 that `info()` throws `FlywaySqlUnableToConnectToDbException` against a closed port. The unit test mocks `info()` to return an empty list, so it passes. A validation failure on a repeatable `R__` file has an empty version (`ValidateOutput.version` is `""` for a repeatable), and `display("")` throws `NumberFormatException` for the same reason.
   - **Fix:** wrap the whole detail lookup in `try { ... } catch (RuntimeException ex) { return FALLBACK_OBJECT; }` and skip null/blank versions before `display`. Add two unit cases: `info()` throws, and `validateResult("")`.
   - **If we skip it:** A database outage at start gives no message ID and no version, and the on-call sees a secondary error; the story's "no version" fallback is not actually exercised.

2. **The lint accepts a `V0000` migration** (`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/rule/SequenceGapRule.java:L30-49`; `ParsedMigrationFile.java:L15`; `NameRule.java:L24-31`)
   - **What this is:** The sequence rule reports missing numbers in the `V0001`..`V<N>` range.
   - **Problem:** A folder holding only `V0000__rwb_e1_044_baseline.sql` gives no finding: the distinct set is `{0}`, the highest is 0, the loop 1..0 is empty, and the name regex accepts `0000`. I reproduced it with the built test classes (`MigrationLint.lint` returned an empty list). The old lint used a running `expected=1` counter and would have flagged it, so this is a regression. Flyway baselines at version 0, so such a file may never be applied.
   - **Fix:** in `SequenceGapRule.checkFolder`, when the set is non-empty and `sequences.first() < 1`, add one `L-SEQ-GAP` finding for the lowest sequence ("sequence must start at V0001"). Add a `t01-seqzero-fail` fixture.
   - **If we skip it:** A migration named `V0000` is accepted and may never run, leaving the schema missing its objects.

## Should fix

3. **The lint silently checks nothing when the folder is missing** (`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/MigrationLint.java:L27-30`)
   - **What this is:** `MigrationLint.lint` returns an empty list when the path is not a directory.
   - **Problem:** The production-folder test uses the relative path `src/main/resources/db/modulemigration/recovery`. Run it from the repository root, rename the folder or lose permission, and the test passes with zero migrations checked. I reproduced `MigrationLint.lint(Path.of("C:/definitely/not/here"))` returning `[]`. A mistyped expected-empty fixture has the same false green.
   - **Fix:** delete the `Files.isDirectory` early return; `list()` already wraps `IOException` in an `UncheckedIOException` that names the folder. The existing empty-`@TempDir` test still passes.
   - **If we skip it:** The lint gate can go green while scanning nothing.

4. **The drift check cannot see a length, precision or enum change** (`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/SchemaSnapshotReader.java:L24-25`; `SchemaComparator.java:L56-58`)
   - **What this is:** The snapshot stores `information_schema.columns.data_type`; the comparator reports a difference only when that string or nullability changes.
   - **Problem:** `varchar(8)` and `varchar(50)` both report `character varying`; `numeric(10,2)` and `numeric(12,2)` both report `numeric`; two different enum types both report `USER-DEFINED`. A real drift returns no difference. The unit test only changes `text` to `varchar(8)`, which does change `data_type`, so it passes.
   - **Fix:** read `pg_catalog.format_type(a.atttypid, a.atttypmod)` (the full type, for example `character varying(8)`) instead of `data_type`, and compare that. Add one unit case with two `varchar` lengths.
   - **If we skip it:** A schema that has changed a column width or an enum is reported as drift-free.

5. **The history-table name is hard-coded twice** (`backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/migration/RecoveryFlywayConfig.java:L28`; `SchemaSnapshotReader.java:L28`)
   - **What this is:** The Flyway config and the drift reader both spell `flyway_schema_history_recovery`.
   - **Problem:** They must change together. If the history table is renamed, the reader starts including Flyway's own bookkeeping; a target that has no history table then shows a false table difference.
   - **Fix:** pass `RecoveryFlywayConfig.HISTORY_TABLE` from the container test into `SchemaSnapshotReader.read` (the test is in the same package), or make one shared constant.
   - **If we skip it:** A future rename makes the drift check noisy or wrong.

## Nice to have

6. **A second `-- Story:` line with leading spaces is not reported** (`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/rule/HeaderMultiRule.java:L23-25`)
   - **What this is:** `L-HEADER-MULTI` looks for a second story header.
   - **Problem:** It uses `startsWith("-- Story:")` on the raw line, so `  -- Story: RWB-E1-028` passes, while `HeaderRule` for line 1 trims with `.strip()`. I reproduced it with a temporary file: zero findings.
   - **Fix:** `lines.get(index).strip().startsWith("-- Story:")`. One line.
   - **If we skip it:** A copied or indented second header goes unreported; low impact because the key comes from the file name.

7. **Dead formatting wrappers** (`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/SchemaComparator.java:L112-114`; `SchemaDifference.java:L20-23`)
   - **What this is:** `SchemaComparator.format` only calls `SchemaDifference.format`, and `SchemaDifference.toString` is never called.
   - **Problem:** Two extra public entry points to keep and test for one format string.
   - **Fix:** delete both; the test calls `difference.format()` directly.
   - **If we skip it:** Seven more lines to read and maintain for no behaviour.

Verdict: fix 1 and 2 first. The Should fixes are small and belong in the same pass.

Lean: -7 lines possible.

Not checked: SIT/UAT/PROD application of the D-RUN-14 grants and real-environment drift (HV-E044-01, D-RCV-05, out of scope); the coverage task is not wired into `check`/CI, so I ran `recoveryCoverageVerification` by hand (PASS, 94.6% line / 86.5% branch).

## Fix round 1 verification (`c253b3c`)

Re-read the fix diff (24 files, +370/−135) and re-ran the checks: `./gradlew test` (all green; 60 lint, 19 lexer, 7 comparator and 9 runner tests), `recoveryIntegrationTest` for `RecoveryMigrationIT` (12/12 green, including the new column-length drift case) and `recoveryCoverageVerification` (PASS; 94.9% line, 86.3% branch). The tests and probes cover the failure path, missing folder, `V0000`, indented header and dynamic GRANT.

| Finding | Verdict | Evidence and residual |
|---|---|---|
| 1. Must — failure report | **Closed** | `failureObject` now wraps the detail lookup in `try/catch` and filters null/blank versions; `aDetailLookupFailure…` and the real `aBrokenConnection…` (port 1) assert the fallback line and the original exception; `display` no longer throws on an empty part. |
| 2. Must — `V0000` | **Closed** | `SequenceGapRule` adds a finding when `first() < 1`; `t01-seqzero-fail` expects `L-SEQ-GAP/V0000/0/V0000`, and the suite is green. |
| 3. Should — missing folder | **Closed** | The early return is gone; `aMissingFolderFailsClosed` expects `UncheckedIOException`; an empty `@TempDir` still gives no finding. |
| 4. Should — drift depth | **Closed for table columns** | `COLUMNS` uses `pg_catalog.format_type`; the unit test covers varchar/numeric/enum and the IT alters `team_code` to `varchar(50)` for one `CHANGED`. Residual: a view column type change is still invisible; `ViewSnapshot` stores names only, and `fromRows` discards the view `ColumnSnapshot`s the query now reads (new 9). |
| 5. Should — history table | **Closed** | `SchemaSnapshotReader.read` takes the table name; the IT passes `RecoveryFlywayConfig.HISTORY_TABLE`; no literal remains in the tooling. |
| 6. Nice — indented header | **Closed** | `HeaderMultiRule.strip()`; `t03-header-multi-indented-fail` passes. |
| 7. Nice — dead lines | **Closed** | `SchemaComparator.format` and `SchemaDifference.toString` are deleted; the test calls `.format()`; the seven lines are gone. |
| 8. New — dynamic-GRANT false positive | **Open (Should fix)** | `GrantRule` flags any statement containing both `EXECUTE` and grant/revoke. The real lint on a valid table and function with quoted columns `"execute"`/`"grant"` returns two `L-GRANT` lines. Fix: match only `EXECUTE` followed by a string that starts with `GRANT`/`REVOKE` (for example `(?is)\bexecute\s+'\s*(?:grant\|revoke)\b`); the two dynamic `t20-grant-fail` fixtures still pass. |
| 9. New — view column types | **Open (Nice)** | A view with `team_code varchar(8)` altered to `varchar(50)` gives no difference. Store the `ColumnSnapshot`s for views (the `COLUMNS` query already returns them) and compare them; not a regression, because the old view model was names only too. |

**Test weakening:** none. The `containsExactly` → `containsExactlyInAnyOrder` on `SchemaSnapshot.tables` is correct because that record is a `Set`; the comparator tests still use ordered `containsExactly`, and no assertion was deleted or relaxed to hide a regression.

**Residual (not a regression):** a real repeatable validation failure with a pending versioned migration would log that pending version, not `recoveryFlyway`; the `anInvalidVersion…` test mocks an empty pending list. It does not crash and repeatables are forbidden by `L-REPEATABLE`.

**Final verdict:** Ship after 8. Findings 1-7 are closed, 9 is a Nice follow-up, and the rest of the extra changes (split qualifier, size/depth bounds) are documented and tested; the security reviewer's two Info residuals (read-before-size-cap and the block-comment memo edge on files that already fail `L-LEX`) remain and are not valid-file bypasses.

## Fix round 2 verification (`a74324a`)

Finding 8 is fixed for the tested cases — `t20-grant-fail` still gives its five findings and the new `t20-grant-quoted-pass` (quoted `"execute"`/`"grant"` columns) gives none — and the two security residuals are closed: the size check runs before `Files.readString` (`anOverLimitFileFailsOnItsSizeBeforeItIsRead` passes) and the block-comment stack gives one `L-LEX` for `/* /* */` while the 100,000-opener case stays linear; `./gradlew test` is green (61 lint, 21 lexer tests) and no test was weakened. But the narrowed `EXECUTE` regex introduces a new dynamic-GRANT bypass: the real lint returns no `L-GRANT` for `EXECUTE $q$GRANT …$q$`, `EXECUTE format('GRANT …')` or `EXECUTE 'x' || 'GRANT …'`, all of which the `c253b3c` broad check caught. That is new finding 10, a regression of SEC-044-03; scan every string literal (single-quoted, `E''`, dollar-quoted, a `format` argument, a concatenation) in a statement that contains an `EXECUTE`, and add one fail fixture for each. **Final verdict: not closed; no ship until 10 is fixed.**

## Closure

The L-GRANT churn is closed by reverting the rule to the gated specification, not by another case. `GrantRule` checks GRANT/REVOKE as the first word of a line (code text, so `-- GRANT` and `/* REVOKE */` pass) and of a statement (statement view (c), so `SELECT 1; GRANT …` fails); `t20-grant-fail` gives its three findings, `t20-grant-pass` and `t20-grant-quoted-pass` pass, and the out-of-spec dynamic-SQL fixtures were removed rather than replaced. The other review fixes remain: missing folder fails closed, split qualifier, failure-info masking, history-table parameter, size pre-check, block-comment stack, full-type drift, V0000 and the dead lines. Unit tests are green (61 lint, 21 lexer, 7 comparator, 9 runner, 6 pin, 5 Flyway); coverage passes all four counters at 94.3 instruction / 86.3 branch / 94.9 line / 98.0 method; no required test was weakened. The dynamic-SQL limitation is gap DG-E044-DYN-01 (SPEC-009 and T-044-20 cited, Blocker No, code review and D-RUN-14 as the control), not a code finding; the intermediate dynamic-SQL findings 10–12 are withdrawn into that gap. The view-column-type Nice (9) remains a follow-up. **Verdict: Ship.**
