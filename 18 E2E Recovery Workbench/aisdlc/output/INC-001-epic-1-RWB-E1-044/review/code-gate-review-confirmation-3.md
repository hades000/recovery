# Code gate review (confirmation round 3): RWB-E1-044

| Field | Value |
|---|---|
| Story | RWB-E1-044, run `INC-001-epic-1-RWB-E1-044` |
| Reviewer | Compliance Reviewer, code gate mode (Claude Opus 5.5, high effort), read only |
| Date | 19 Nov 2026 |
| Diff range | `a241338..f319748` (round 3 changes), branch `fix/REVIEW-001-e1-044-confirmation`, base `27567ed`, worktree `rwb-wt/REVIEW-001-E1-044` |
| Previous gate | `review/code-gate-review-confirmation-2.md`, FAIL 0C/0H/1M/3L (CONF2-E044-01..04) |
| Measured against | `specify/spec.md` SPEC-003, SPEC-007; AGENTS.md §3.10, §3.16, §4.5 |
| Rule | D-RUN-09: any finding, Low included, fails the gate |

## 1. What I ran

- `./gradlew test --rerun` in the worktree `backend` at `f319748`: BUILD SUCCESSFUL, 49 suites, 436 tests, 0 failed, 0 errors, 0 skipped.
- 18 probe migrations in my scratchpad, linted with `MigrationLint.lint` on the compiled classes through jshell, plus the round-2 `ON_OBJECT` pattern applied to three of them for comparison. No repository file was changed.
- Not run: `dev.ps1 up`, `it`, `e2e`. The builder's `final-gate-2-it-RecoveryMigrationIT.log` (12/12, timestamp after `608b44a`) shows the part-way failure still names version 2, now only through the callback.

## 2. Previous findings

| ID | Status | Evidence |
|---|---|---|
| CONF2-E044-01 | Closed (for the kinds listed); see CONF3-E044-03 for `CAST` | `COMMENT_ON`, `LiteralSchemaRule.java:69-70, 105`. Fixture `t02-comment-on-kinds-fail` (14 lines, qualifier `rwb_case`), `RecoveryMigrationLintTest.java:159, 244-250`. Red `b5da0b4` before green `7426619`; `conf2-01-red.log` fails that fixture; `conf2-01-mutation-comment-on-removed-red.log` fails it with `COMMENT_ON` removed (AGENTS §3.16). Probes: multi-line `COMMENT ON INDEX` and `COMMENT ON OPERATOR rwb_case.+` are reported; `COMMENT ON TRIGGER/CONSTRAINT ... ON t1`, `IS NULL` and string text give no finding |
| CONF2-E044-02 | Closed | `COLUMN` left `POSITION`; `COMMENT_COLUMN`, `LiteralSchemaRule.java:76-77, 106`. Fixture `t02-comment-column-pass`; `t02-unknown-positions-fail` line 20 still fails. Red `afc377d` before green `4cdbcd8`; mutation log shows only line 20 depends on `COMMENT_COLUMN`. Probes: quoted `"rwb_case"."t1"."c"` and spaced `rwb_case . t1 . c` are reported |
| CONF2-E044-03 | Closed (for the probes named); see CONF3-E044-01 and -02 | `ON_OBJECT`, `LiteralSchemaRule.java:55-57`, first `ON` after the prefix only. Both round-2 probes added to `t02-join-alias-pass` lines 8-9. Red `b8eecf0` before green `4af496b`; `conf2-03-mutation-any-on-red.log`. Probes: `CREATE TRIGGER ... ON t1 ... WHEN (... JOIN ... ON a.id = b.id)` passes; `ON ONLY`, `UPDATE OF a ON`, `DROP RULE IF EXISTS`, `CREATE POLICY p1 ON rwb_case.t1`, an `on_date` column are reported |
| CONF2-E044-04 | Closed | No `org.flywaydb.core.internal` import. `FailedVersion` callback on `AFTER_EACH_MIGRATE_ERROR`, `RecoveryMigrationRunner.java:83-87, 105-130`, registered at `RecoveryFlywayConfig.java:48` and asserted by `RecoveryFlywayConfigTest.java:52-53`. ArchUnit rule `RecoveryMigrationRunnerTest.java` `theMigrationCodeUsesOnlyThePublicFlywayApi` (main classes of the package only; ArchUnit fails on an empty import by default). Red `fc53c9b` (`conf2-04-red.log`: rule violated once) before green `608b44a` |

Callback checks (requested): one `FailedVersion` per `recoveryFlyway` bean, `volatile` field; `migrate()` runs once per bean through `initMethod`, and a failure discards the context, so no version carries over between runs in production. When no callback fired, `failureObject` returns `recoveryFlyway` (unit tests at lines 114 and 132, and the real-Flyway `aBrokenConnectionStillLogsTheFallbackAndRethrows`). A lookup failure still falls back (`aDetailLookupFailure...`, now on `getConfiguration()`; the validation path keeps its `info()` call inside the same `catch`). No test was weakened: the stubs of `info()` that remain in the non-validation tests act as decoys and show that the pending list is no longer used.

## 3. New findings

| ID | Severity | Where | Defect | Required fix |
|---|---|---|---|---|
| CONF3-E044-01 | Low | `LiteralSchemaRule.java:57` (`(?:(?!\bON\b)[^;])*`, added in `4af496b`); `README.md:59-60` | New false negative. The tempered token stops at any word `on`, also inside a quoted identifier, and the match then fails. `CREATE TRIGGER "audit on insert" AFTER INSERT ON rwb_case.t1 FOR EACH ROW EXECUTE FUNCTION f1();` and `CREATE INDEX "on" ON rwb_case.t1 (a);` give no finding at `f319748`; the round-2 pattern reports `rwb_case` for both. The README says the first `ON` after the prefix is checked | Skip quoted identifiers in the token, for example `(?:"(?:[^"]\|"")*"\|(?!\bON\b)[^;"])*`. Add both probe lines, qualifier `rwb_case`, to a failing fixture |
| CONF3-E044-02 | Low | `LiteralSchemaRule.java:52-57`; `README.md:61` | `CREATE [OR REPLACE] RULE r1 AS ON INSERT TO rwb_case.t1 DO INSTEAD NOTHING;` gives no finding: the target table after `TO` is checked nowhere. It was not reported at `a241338` either and `TO` is not in the SPEC-007 item-1 minimum, but the lint extends item 1 to rules (`ALTER`/`DROP RULE ... ON` are checked), AC5 says a literal qualifier fails, and the README now describes `CREATE RULE` without saying its table is unchecked. The round-2 required fix ("for `CREATE RULE` none") did not cover this position | Report the qualifier after `CREATE [OR REPLACE] RULE <name> AS ON <event> TO`. Add a failing fixture line with `rwb_case` that no broader check reports (AGENTS §3.16). Or record the gap as an assumption and say it in the README |
| CONF3-E044-03 | Low | `LiteralSchemaRule.java:69-70` | `COMMENT ON CAST (rwb_case.ty1 AS int) IS 'x';` gives no finding: the `(` ends the `NAME\s+` run, and only the target type is caught (by `AS`). The implementation report says `COMMENT ON <kind>` now holds for every kind, as CONF2-E044-01 required | Report the source type qualifier of `COMMENT ON CAST (`, and add a failing fixture line. Or narrow the claim in the implementation report and record the excluded kind |

## 4. Other checks

| Check | Result | Notes |
|---|---|---|
| Unit tests | PASS | 436/0/0/0 on `--rerun`, matching `final-gate-2.log` |
| Red before green | PASS | Four red commits, each before its green commit, each with a failing log |
| Tests weakened or skipped | PASS | No `@Disabled` or skip; changed runner tests still assert the exact `MSG-P3-016` line |
| False positives on `V0001` and pass fixtures | PASS | All green; `COMMENT ON COLUMN c1.note` and the join probes pass |
| Dependencies, merged migrations | PASS | No build file or migration changed |
| PII and literals | PASS | Synthetic names only |
| Coverage | PASS | Backend 90.82% instruction, 81.04% branch, 91.10% line, 95.90% method (builder `final-gate-2.log`; my run regenerated the report and exited 0). Frontend NOT_APPLICABLE |
| Commit trailers (AGENTS §4.12) | PASS | All nine commits carry `Co-Authored-By: Claude Opus 5.5` and the AISDLC trailers |

REVIEW_TYPE: CODE_GATE_REVIEW (CONFIRMATION ROUND 3)
CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 3]
