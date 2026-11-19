# Code gate review (confirmation round 2): RWB-E1-044

| Field | Value |
|---|---|
| Story | RWB-E1-044, run `INC-001-epic-1-RWB-E1-044` |
| Reviewer | Compliance Reviewer, code gate mode (Claude Opus 5.5, high effort), read only |
| Date | 19 Nov 2026 |
| Diff range | `27567ed..a241338`, branch `fix/REVIEW-001-e1-044-confirmation`, worktree `rwb-wt/REVIEW-001-E1-044` |
| Previous gate | `review/code-gate-review-confirmation.md`, FAIL 0C/0H/3M/6L (CONF-E044-01..09) |
| Measured against | `specify/spec.md` (SPEC-003, -007, -009, -010), `plan/plan.md`, AGENTS.md §3, §4, §11 |
| Rule | D-RUN-09: any finding, Low included, fails the gate |

## 1. What I ran

- `./gradlew test --rerun` in the worktree `backend`: BUILD SUCCESSFUL, 432 tests, 0 failed, 0 errors, 0 skipped. The real `V0001` lints clean (`migrationsFollowTheRecoveryRules`).
- 16 probe migrations in my scratchpad, linted with `MigrationLint.lint` on the compiled classes through jshell. No repository file was changed.
- `javap` on `flyway-core-12.4.0.jar` to check the CONF-04 claim.
- Not run: `dev.ps1 up`, `it`, `e2e` (the builder's `conf-04-it-RecoveryMigrationIT.log` shows 12/12).

## 2. Previous findings

| ID | Status | Evidence |
|---|---|---|
| CONF-E044-01 | Closed | Fixture `t02-unknown-positions-fail` (26 lines, qualifier `rwb_case`), `RecoveryMigrationLintTest.java:149, 224-236`. Red `4dc5c33` before green `fad5e70`; `conf-01-red.log` fails on line 20. `conf-01-mutation-position-removed-red.log`: with the POSITION collector removed only this fixture fails. Every form the previous gate listed is present. The remaining `COMMENT ON <kind>` gap is new finding CONF2-E044-01 |
| CONF-E044-02 | Closed | `LiteralSchemaRule.java:57-69, 110-135` (CREATE TABLE column list, `ADD [COLUMN]`; `ALTER COLUMN ... TYPE` by the `TYPE` position). Fixtures `t02-column-type-fail` and `-pass`, `LintTest:152-154`. Red `f529731` before green `16abbdc`. Probes: a `','` default and `LIKE rwb_case.src` behave correctly |
| CONF-E044-03 | Closed | `GrantRule.java:26, 55-58`: `(?i)\s*(?:GRANT\|REVOKE)\b` with `lookingAt()` on both views. Fixtures `t20-grant-tab-fail` and `t20-grant-word-pass`, `LintTest:173-175`. Red `fa150b8` before green `46844fe` |
| CONF-E044-04 | Closed (behaviour); see ruling 3(a) and CONF2-E044-04 | `RecoveryMigrationRunner.java:76-78`. New test `RecoveryMigrationRunnerTest.java:121` (pending 2 and 3, plain `FlywayException`, object `recoveryFlyway`). Red `354410f` before green `2590774`; `conf-04-red.log` shows `object=2` |
| CONF-E044-05 | Closed | `MigrationPropertiesConfigTest.java:64, 70`. No production change, so no red-before-fix run is possible; `conf-05-mutation-notnull-and-case-red.log` shows both tests fail with `@NotNull` removed and the pattern made `(?i)`. Commit `5200540` |
| CONF-E044-06 | Closed | DEV-E044-05 appended to `implement/deviations.md` (`c1f54f4`). OPEN-060 is in `aisdlc/docs/open-items.md:48` on develop-recovery |
| CONF-E044-07 | Closed (for the forms fixed); see ruling 3(b) and CONF2-E044-03 | Bare `ON` removed; `ON_OBJECT`, `LiteralSchemaRule.java:53-55`. Fixture `t02-join-alias-pass`, `LintTest:157`. Red `5850522` before green `0a9b2a9`. `README.md:59-61` updated |
| CONF-E044-08 | Closed | `implement/code-map.md:32` CODE-E044-028 now says 55 folders at `b1d7424`, with a dated orchestrator correction note |
| CONF-E044-09 | Closed | Run `README.md:57-70` "Provenance (orchestrator correction, 19 Nov 2026)"; `AI-SDLC-BUILD-LOG.md` rows 520 (00:02 correction), 532 and 549 |

Note: the CONF-E044-08 correction, OPEN-060, the AGENTS.md entry and the log rows are uncommitted working-tree changes on develop-recovery at the time of this review. The orchestrator should commit them at its next checkpoint.

## 3. Rulings on the builder's judgement calls

**(a) CONF-04, pending lookup kept for `FlywayMigrateException` and for a validation failure that names no version.**
The behaviour meets the SPEC-003 table. A failed migration is the "fails part way" row, and a lower pending version under `outOfOrder(false)` is a validation failure whose version is mandatory, so falling through to `pending()[0]` is right; the existing test `RecoveryMigrationRunnerTest.java:78` covers it. Every other `FlywayException` now reports `recoveryFlyway`. I confirmed with `javap` that `FlywayMigrateException` sets no public error code (`getErrorCode()` stays `ERROR`; only the internal `getMigrationErrorCode()` gives `FAILED_VERSIONED_MIGRATION`).
But the type is in `org.flywaydb.core.internal`, and SPEC-003 (ASM-E044-12) expects the public Flyway API. A public route exists: a `Callback` on `Event.AFTER_EACH_MIGRATE_ERROR` receives the failing `MigrationInfo`. The internal import is explained only in the implementation report, not as a deviation. That is finding CONF2-E044-04 (Low). The behaviour itself is accepted.

**(b) CONF-07, bare `ON` removed, bare `AS` kept.**
Keeping `AS` is accepted. SPEC-007 item 2 names `AS` inside `CAST(`, and the list "may extend but not narrow". An alias is never written as `AS a.b`. My probes (column aliases, `AS t2`, `NEW.a AS b`, `CREATE VIEW ... AS SELECT a.id`, a plpgsql `AS $$ ... $$` body) and `V0001` (`AS v(...)`, `AS e(...)`) give no finding, and `CREATE DOMAIN rwb_case.d1 AS int` is still reported.
Removing bare `ON` is accepted, but the replacement `ON_OBJECT` still reaches a join `ON` in two forms. That is finding CONF2-E044-03.

## 4. New findings

| ID | Severity | Where | Defect | Required fix |
|---|---|---|---|---|
| CONF2-E044-01 | Medium | `LiteralSchemaRule.java:44-55` | SPEC-007 item 1 lists `COMMENT ON <kind>` as a position. Only kinds that share a POSITION keyword (TABLE, VIEW, SEQUENCE, FUNCTION, TYPE, DOMAIN, COLUMN) or an `... ON` form are covered. Probes: `COMMENT ON INDEX rwb_case.i1`, `COMMENT ON AGGREGATE rwb_case.a(int)`, `COMMENT ON ROUTINE rwb_case.f()`, `COMMENT ON COLLATION rwb_case.c` and `COMMENT ON STATISTICS rwb_case.s` give no finding. The gap was there before the fix, but the implementation report says "every SPEC-007 item-1 position" is covered. No deviation is recorded ("may extend but not narrow") | Report the schema qualifier of the object name after `COMMENT ON <kind>` for every kind. Add failing fixtures with an unknown qualifier, at least `COMMENT ON INDEX rwb_case.i1`. Or record a deviation with spec-gate approval |
| CONF2-E044-02 | Low | `LiteralSchemaRule.java:45` (`COLUMN` added in `fad5e70`) | `COMMENT ON COLUMN c1.note IS 'x';` (table.column, no schema) is reported as `literal schema c1`. In that form the first part is the table, not a schema. Unqualified names are allowed (SPEC-008: they resolve to `recovery`). This false positive is new and not documented | Under `COLUMN`, report only the first part of a three-part name (`s.t.c`). Add a passing fixture `COMMENT ON COLUMN c1.note` and keep `rwb_case.t1.id` failing |
| CONF2-E044-03 | Low | `LiteralSchemaRule.java:53-55`; `README.md:59-61` | `[^;]*?\bON` takes the first *qualified* `ON` before `;`. When the object-name `ON` is not qualified, a later join `ON` is reported. Probes: `CREATE RULE r AS ON INSERT TO ${recoverySchema}.t DO ALSO INSERT ... JOIN ... b ON a.id = b.id;` gives `literal schema a`, and `CREATE POLICY p ON t USING (EXISTS (... JOIN ... v ON u.id = v.id));` gives `literal schema u`. The README says a join condition passes | Check only the object-name `ON`: the first `ON` after the INDEX/TRIGGER/POLICY/CONSTRAINT/GRANT prefix, and for `CREATE RULE` none (its event `ON` is not an object). Add passing fixtures for both probes. Or document the false positive as an assumption |
| CONF2-E044-04 | Low | `RecoveryMigrationRunner.java:9, 76`; `RecoveryMigrationRunnerTest.java` (`migrateFailure`) | Production code imports `org.flywaydb.core.internal.exception.FlywayMigrateException`. SPEC-003 (ASM-E044-12) expects the public Flyway 12.4.0 API, and a public route exists (`Event.AFTER_EACH_MIGRATE_ERROR` callback). The choice is recorded only in the implementation report, not as a deviation | Use the public callback, or append DEV-E044-06 to `implement/deviations.md` (internal type, why, compile-time failure on upgrade, `RecoveryMigrationIT` as proof) for the spec owner to accept |

## 5. Other checks

| Check | Result | Notes |
|---|---|---|
| Unit tests | PASS | 432/0/0/0 on `--rerun`, matching `final-gate.log` |
| Red before green | PASS | Each red commit comes before its green commit and has a failing log (CONF-01, -02, -03, -04, -07). CONF-05 is test-only, with a mutation log |
| Tests weakened or skipped | PASS | No `@Disabled` or skip added. The two runner tests that now throw `FlywayMigrateException` still exercise the lookup |
| False positives on `V0001` and existing pass fixtures | PASS | All green. New false positives are CONF2-E044-02 and -03 |
| Dependencies | PASS | No build file changed |
| PII and literals | PASS | Synthetic names only (`rwb_case`, `c1`, `rwb_migrator`). No business literal added |
| Coverage | PASS | Bundle 90.80% instruction, 81.01% branch, 91.13% line, 95.85% method (`recoveryCoverageReport.xml`). Frontend NOT_APPLICABLE (no frontend file changed) |
| Commit trailers (AGENTS §4.12) | PASS | Claude Opus 5.5, which matches the builder named in the report |

REVIEW_TYPE: CODE_GATE_REVIEW (CONFIRMATION ROUND 2)
CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 3]
