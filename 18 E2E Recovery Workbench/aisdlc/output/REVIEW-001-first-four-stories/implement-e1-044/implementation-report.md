# Implementation report: RWB-E1-044 code gate confirmation fixes (REVIEW-001)

| Field | Value |
|---|---|
| Run | `REVIEW-001-first-four-stories` (stage `implement`) |
| Input | `INC-001-epic-1-RWB-E1-044/review/code-gate-review-confirmation.md`, `CODE_GATE: FAIL [C:0] [H:0] [M:3] [L:6]` |
| Spec / plan | `INC-001-epic-1-RWB-E1-044/specify/spec.md` (SPEC-002, -003, -007, -009, -010), `plan/plan.md` |
| Branch | `fix/REVIEW-001-e1-044-confirmation` from `develop-recovery` at `27567ed`, local only |
| Builder | Claude Code, Claude Opus 5.5 (Implementation Builder) |
| Scope | CONF-E044-01 to -07. CONF-E044-08 and -09 belong to the orchestrator and were not touched |
| Date | 19 Nov 2026 |

## Findings, fixes and evidence

All logs are in this folder. A "red" log is the failing run committed before the fix; a "green"
log is the run after it.

| Finding | Fix | Commits | Evidence |
|---|---|---|---|
| CONF-E044-01 (M) | New fixture `t02-unknown-positions-fail`: every SPEC-007 item-1 position (`TABLE`, quoted `"rwb_case".t2`, `VIEW`, `MATERIALIZED VIEW`, `SEQUENCE`, `INDEX … ON`, `TRIGGER … ON`, `FUNCTION`, `PROCEDURE`, `TYPE`, `DOMAIN`, `REFERENCES`, `FROM`, `JOIN`, `INTO`, `UPDATE`, `TRUNCATE`, `COMMENT ON TABLE/COLUMN/CONSTRAINT … ON`, `POLICY … ON`, `OWNED BY`, `GRANT … ON`) and item-2 form (`::`, `CAST(… AS …)`) with the unknown qualifier `rwb_case`; the test asserts the complete list. The fixture exposed a real gap, `COMMENT ON COLUMN rwb_case.t1.id`, fixed by adding `COLUMN` to the position keywords. | `4dc5c33` red, `fad5e70` green (`GRANT … ON` line added in `0a9b2a9`) | `conf-01-red.log` (line 20 missing), `conf-01-green.log`, `conf-01-mutation-position-removed-red.log`: with the `POSITION` collector line removed, `t02-unknown-positions-fail` fails and every other test stays green; the line was restored before the green commit |
| CONF-E044-02 (M) | `LiteralSchemaRule` checks a column data type: each top-level element of a `CREATE TABLE` column list (nested parentheses skipped) and `ALTER TABLE … ADD [COLUMN] [IF NOT EXISTS] c type`. `ALTER COLUMN … [SET DATA] TYPE` was already reported by the `TYPE` position and is now asserted. The rule now returns its findings in line order. Fixtures `t02-column-type-fail` (7 findings) and `t02-column-type-pass` (allowed and unqualified types, `numeric(18, 2)`, constraints, `count(DISTINCT c.id)`). | `f529731` red, `16abbdc` green | `conf-02-red.log` (lines 2, 5, 7, 8, 9 missed), `conf-02-green.log` |
| CONF-E044-03 (M) | `GrantRule` matches `(?i)\s*(GRANT\|REVOKE)\b` with `lookingAt()` for both the code-text line and the statement's first word. Fixtures `t20-grant-tab-fail` (`GRANT<TAB>` and `REVOKE<TAB>` inside a `DO $$` body and an indented `$body$` function body) and `t20-grant-word-pass` (`granted_at`, `revoked_by`, `grantee`). | `fa150b8` red, `46844fe` green | `conf-03-red.log` (no finding at all), `conf-03-green.log` |
| CONF-E044-04 (L) | `RecoveryMigrationRunner.failureObject` reads `info().pending()` only for the two versioned rows of the SPEC-003 table: a `FlywayValidateException` whose validate result names no version (a lower pending version) and a migration that failed while running (`FlywayMigrateException`, what Flyway 12.4.0's `DbMigrate` throws). Any other `FlywayException` reports `recoveryFlyway`. New unit test: a lock-timeout `FlywayException` while `pending()` holds 2 and 3 reports `recoveryFlyway`. The part-way and lookup-failure tests now throw `FlywayMigrateException`, so they still exercise the lookup. | `354410f` red, `2590774` green | `conf-04-red.log` (`object=2`), `conf-04-green.log`, `conf-04-it-RecoveryMigrationIT.log` (`recoveryIntegrationTest --tests *RecoveryMigrationIT`, Testcontainers, 12/12, including the part-way failure, lower pending version and checksum cases) |
| CONF-E044-05 (L) | `MigrationPropertiesConfigTest` gains `anAbsentSchemaFailsAtPropertiesBinding` and `aSchemaThatDiffersOnlyInCaseFailsAtPropertiesBinding`, each asserting the `ConfigurationPropertiesBindException` for `RecoveryMigrationProperties` and the `BindValidationException` root naming `rwb.schema` and `D-RCV-28` (and `[Recovery]` as the rejected value). No production change was needed, so there is no red-before-fix run. | `5200540` | `conf-05-green.log` (8/8); `conf-05-mutation-notnull-and-case-red.log`: with `@NotNull` removed and the pattern made `(?i)`, exactly the two new tests fail and the six earlier ones stay green. The record was restored before the commit |
| CONF-E044-06 (L) | Caps unchanged. DEV-E044-05 appended to `INC-001-epic-1-RWB-E1-044/implement/deviations.md`, dated 19 Nov 2026 and naming the confirmation review: the 262,144-byte and depth-32 caps, fail-closed behaviour, and the RWB-E1-001 consequence (a single-file baseline from the 925,733-byte Physical Schema v6 is rejected; split the files or raise the cap with a recorded reason). The proposed open item is in `shared-updates.md` in this folder. | `c1f54f4` | Documentation only |
| CONF-E044-07 (L) | The bare `ON` position is removed. A new `ON_OBJECT` pattern checks the qualifier after `ON` only in `CREATE/ALTER/DROP/COMMENT ON … INDEX/TRIGGER/POLICY/RULE/CONSTRAINT … ON` and in `GRANT/REVOKE … ON`, stopping at the statement's `;`. `AS` is kept: no alias false positive exists (an alias is never followed by a dot), and the bare form also covers `CREATE DOMAIN d AS q.t`. Fixture `t02-join-alias-pass` (column aliases, `AS a`, `CAST(a.id AS text)`, `ON a.id = b.id`, `ON` split from `c.id` by a newline). No expected finding was lost, so no assumption was needed. The migration folder `README.md` states the narrowed rule. `V0001` was not edited. | `5850522` red, `0a9b2a9` green | `conf-07-red.log` (reported `a` line 5 and `c` line 7), `conf-07-green.log` (`t02-unknown-positions-fail` still reports every `… ON rwb_case.t1` form) |

## Final gate run

Command, in `backend`: `./gradlew test recoveryCoverageReport recoveryCoverageVerification`, exit 0
(`final-gate.log`). `recoveryCoverageVerification` executed in that run.

| Surface | Status | Tests | Instruction | Branch | Line | Method |
|---|---|---|---|---|---|---|
| Backend | REQUIRED | 432 passed, 0 failed, 0 skipped (49 suites) | 90.80% (14153/15587) | 81.01% (1301/1606) | 91.13% (2608/2862) | 95.85% (555/579) |
| Frontend | NOT_APPLICABLE | N/A: no frontend file changed | N/A | N/A | N/A | N/A |

Counters are the `BUNDLE` totals of `recoveryCoverageReport.xml` (copied into this folder). Each is
at or above 0.80. Integration: `RecoveryMigrationIT` 12/12 through `recoveryIntegrationTest`.

## Files changed

- Main: `casewf/migration/RecoveryMigrationRunner.java`; `db/modulemigration/recovery/README.md`.
- Test tooling: `architecture/migration/rule/LiteralSchemaRule.java`, `rule/GrantRule.java`.
- Tests: `RecoveryMigrationLintTest.java`, `RecoveryMigrationRunnerTest.java`,
  `MigrationPropertiesConfigTest.java`; six new fixture folders under `migration-lint/` (55 to 61;
  `RecoveryMigrationLintTest` 61 to 67 tests)
  (`t02-unknown-positions-fail`, `t02-column-type-fail`, `t02-column-type-pass`, `t02-join-alias-pass`,
  `t20-grant-tab-fail`, `t20-grant-word-pass`).
- Evidence: `INC-001-epic-1-RWB-E1-044/implement/deviations.md` (appended), this folder.

## Notes for the re-gate

- `RecoveryMigrationRunner` imports `org.flywaydb.core.internal.exception.FlywayMigrateException`.
  Flyway 12.4.0 has no public type for a failed migration (its `getErrorCode()` is the generic
  `ERROR`), so the internal class is the only discriminator. The version is pinned and
  `RecoveryMigrationIT` proves the behaviour against the real Flyway. A Flyway upgrade that moves the
  class fails compilation, not silently.
- The validation fall-through to the pending version is kept: SPEC-003 makes the version mandatory
  for a lower pending version under `outOfOrder(false)`, which is a validation failure.
- The column-type check reads lexically. `CREATE TABLE … AS SELECT count(DISTINCT a.id)` has no
  column list and is not affected. A generated-column expression `(CASE a.b …)` sits inside nested
  parentheses and is skipped.
- No new dependency; no merged migration edited; no shared register edited; no personal data.

## Confirmation round 2 (CONF2-E044-01 to -04)

Input: `INC-001-epic-1-RWB-E1-044/review/code-gate-review-confirmation-2.md`,
`CODE_GATE: FAIL [C:0] [H:0] [M:1] [L:3]`, diff range `27567ed..a241338`. Each finding was fixed
red then green on the same branch. The "Notes for the re-gate" bullet above about
`FlywayMigrateException` is superseded by CONF2-E044-04 below.

### CONF2-E044-01 (M): `COMMENT ON <kind>` for every kind

- Fix: `LiteralSchemaRule` gains `COMMENT_ON`, which reports the first qualified name within the
  kind words after `COMMENT ON` (up to four words, so `TEXT SEARCH CONFIGURATION` and
  `CONSTRAINT k ON DOMAIN` are reached). `COLUMN` is left to `COMMENT_COLUMN` (CONF2-E044-02).
  `ON_OBJECT` no longer carries the `COMMENT ON` prefix or the `CONSTRAINT` kind.
- Fixture: `t02-comment-on-kinds-fail` (failing): `COMMENT ON INDEX`, `AGGREGATE`, `ROUTINE`,
  `COLLATION`, `STATISTICS`, `CONVERSION`, `TEXT SEARCH CONFIGURATION`, `OPERATOR CLASS`,
  `OPERATOR FAMILY`, `CONSTRAINT ... ON DOMAIN`, `TRIGGER ... ON`, `POLICY ... ON`, `RULE ... ON`
  and lower-case `index`, each qualified by the unknown `rwb_case`.
- Commits: `b5da0b4` red, `7426619` green.
- Evidence: `conf2-01-red.log` (only lines 11 to 14 reported), `conf2-01-green.log`,
  `conf2-01-mutation-comment-on-removed-red.log` (with `COMMENT_ON` removed,
  `t02-comment-on-kinds-fail` and `t02-unknown-positions-fail` line 21 fail).
- Status: fixed for every kind except `CAST`; see CONF3-E044-03 below, which narrows this claim.
  No deviation is needed.

### CONF2-E044-02 (L): `COMMENT ON COLUMN t.c` has no schema

- Fix: `COLUMN` leaves the `POSITION` keyword list. A new `COMMENT_COLUMN` pattern matches
  `COMMENT ON COLUMN s.t.c` and reports `s`; in the two-part `t.c` form the first part is the table
  and nothing is reported (SPEC-008: unqualified names resolve to `recovery`).
- Fixture: `t02-comment-column-pass` (passing): `COMMENT ON COLUMN c1.note IS 'x';`.
  `t02-unknown-positions-fail` still reports `COMMENT ON COLUMN rwb_case.t1.id` (line 20).
- Commits: `afc377d` red, `4cdbcd8` green.
- Evidence: `conf2-02-red.log` (`literal schema c1` reported), `conf2-02-green.log`,
  `conf2-02-mutation-comment-column-removed-red.log` (with `COMMENT_COLUMN` removed, only
  `t02-unknown-positions-fail` line 20 fails).
- Status: fixed.

### CONF2-E044-03 (L): only the object-name `ON` is checked

- Fix: `ON_OBJECT` checks only the first `ON` after the `INDEX`, `TRIGGER`, `POLICY`,
  `ALTER/DROP RULE`, `GRANT` or `REVOKE` prefix. `CREATE RULE` is no longer a prefix (its `ON`
  names an event, not an object). The migration-folder `README.md` describes the `ON`,
  `COMMENT ON <kind>` and `COMMENT ON COLUMN` behaviour.
- Fixtures: `t02-join-alias-pass` gains both gate probes, `CREATE RULE ... JOIN ... b ON a.id = b.id`
  (line 8) and `CREATE POLICY p1 ON t1 USING (... JOIN ... v ON u.id = v.id)` (line 9).
  `t02-unknown-positions-fail` gains `DROP RULE` and `ALTER RULE ... ON rwb_case.t1` (lines 27, 28),
  which stay reported.
- Commits: `b8eecf0` red, `4af496b` green.
- Evidence: `conf2-03-red.log` (`literal schema a` and `u` reported), `conf2-03-green.log`,
  `conf2-03-mutation-any-on-red.log` (restoring the old any-`ON` search fails `t02-join-alias-pass`).
- Status: fixed. No assumption is needed.

### CONF2-E044-04 (L): public Flyway API only

- Fix: `RecoveryMigrationRunner` no longer imports `org.flywaydb.core.internal`.
  `RecoveryFlywayConfig` registers `RecoveryMigrationRunner.FailedVersion`, a public `Callback` on
  `Event.AFTER_EACH_MIGRATE_ERROR`; Flyway 12.4.0 fires it with the failing migration's
  `MigrationInfo` before it throws. A non-validation failure reports that version, or
  `recoveryFlyway` when the callback did not fire. The validation path is unchanged.
- Tests: an ArchUnit check in `RecoveryMigrationRunnerTest` (no production class in the migration
  package depends on `org.flywaydb.core.internal`); the unit tests drive the callback instead of the
  internal exception (`RecoveryMigrationRunnerTest` 10 to 12 tests); `RecoveryFlywayConfigTest`
  asserts the callback registration.
- Commits: `fc53c9b` red, `608b44a` green.
- Evidence: `conf2-04-red.log` (ArchUnit fails on `FlywayMigrateException`), `conf2-04-green.log`,
  `conf2-04-it-RecoveryMigrationIT.log` and `final-gate-2-it-RecoveryMigrationIT.log`
  (Testcontainers, 12/12; the part-way failure still names version 2).
- Status: fixed through the public callback, so DEV-E044-06 is not needed.

### Final gate run (round 2)

Command, in `backend` at `608b44a`:
`./gradlew test --rerun recoveryCoverageReport recoveryCoverageVerification`, exit 0
(`final-gate-2.log`); `recoveryCoverageVerification` executed in that run.
Integration: `./gradlew recoveryIntegrationTest --rerun --tests *RecoveryMigrationIT`, exit 0,
12/12 through Testcontainers (`final-gate-2-it-RecoveryMigrationIT.log`). `scripts/dev.ps1 up` was
not used.

| Surface | Status | Tests | Instruction | Branch | Line | Method |
|---|---|---|---|---|---|---|
| Backend | REQUIRED | 436 passed, 0 failed, 0 skipped (49 suites) | 90.82% (14234/15673) | 81.04% (1308/1614) | 91.10% (2620/2876) | 95.90% (561/585) |
| Frontend | NOT_APPLICABLE | N/A: no frontend file changed | N/A | N/A | N/A | N/A |

`recoveryCoverageReport.xml` in this folder is replaced by the round-2 report. Each counter is at or
above 0.80. Tests grew from 432 to 436: two lint fixtures (`t02-comment-on-kinds-fail`,
`t02-comment-column-pass`) and two runner tests.

Files changed in round 2: `RecoveryMigrationRunner.java`, `RecoveryFlywayConfig.java`,
`LiteralSchemaRule.java`, the migration-folder `README.md`; tests `RecoveryMigrationLintTest.java`,
`RecoveryMigrationRunnerTest.java`, `RecoveryFlywayConfigTest.java`; fixtures
`t02-comment-on-kinds-fail` and `t02-comment-column-pass` (new), `t02-join-alias-pass` and
`t02-unknown-positions-fail` (extended). No dependency, merged migration or shared register changed;
no personal data.

## Confirmation round 3 (CONF3-E044-01 to -03)

Input: `INC-001-epic-1-RWB-E1-044/review/code-gate-review-confirmation-3.md`,
`CODE_GATE: FAIL [C:0] [H:0] [M:0] [L:3]`, on `f319748`. Per the orchestrator's churn rule, no
pattern case beyond these three was added.

### CONF3-E044-01 (L): a quoted name containing `on` before the object `ON`

- Fix: the `ON_OBJECT` token that runs to the first `ON` after the prefix now skips a quoted
  identifier whole (`"(?:[^"]|"")*"`), so the word `on` inside `"audit on insert"` or `"on"` is not
  taken for the object `ON`. String literals are already blanked in the identifier text the rule
  reads, so no second view was needed.
- Fixture: `t02-on-quoted-name-fail` (failing): `CREATE TRIGGER "audit on insert" AFTER INSERT ON
  rwb_case.t1 ...` and `CREATE INDEX "on" ON rwb_case.t2 (a)`, each reported as `rwb_case`.
- Commits: `05af35d` red, `c94e183` green.
- Evidence: `conf3-01-02-red.log` (no finding for the fixture), `conf3-01-02-green.log`.
- Status: fixed.

### CONF3-E044-02 (L): the table after `TO` in `CREATE RULE`

- Fix: a new `RULE_TO` pattern reports the qualifier after
  `CREATE [OR REPLACE] RULE r AS ON <event> TO`. The event `ON` itself is still not checked.
- Fixture: `t02-create-rule-to-fail` (failing): `CREATE OR REPLACE RULE r1 AS ON INSERT TO
  rwb_case.t1 ...` and `CREATE RULE r2 AS ON UPDATE TO rwb_case.t2 ...`. No other check reports
  either line.
- Commits: `05af35d` red, `c94e183` green (shared with CONF3-E044-01).
- Evidence: `conf3-01-02-red.log` (no finding for the fixture), `conf3-01-02-green.log`.
- Status: fixed. The migration-folder `README.md` states that the `TO` table is checked.

### CONF3-E044-03 (L): `COMMENT ON CAST` (known limitation, no code)

- The claim is narrowed. `COMMENT ON <kind>` is checked for every kind except `CAST`: in
  `COMMENT ON CAST (s.t AS u)` the source type `s.t` is not checked. The target type after `AS` is
  still reported by the `AS` position. This is a known limitation of the lexical rule, stated in the
  migration-folder `README.md` (commit `c94e183`) and in the CONF2-E044-01 status above.
- Status: closed by narrowing the claim; no code change, as the orchestrator directed.

### Final gate run (round 3)

Command, in `backend` at `c94e183`:
`./gradlew test --rerun recoveryCoverageReport recoveryCoverageVerification`, exit 0
(`final-gate-3.log`); `recoveryCoverageVerification` executed in that run.
Integration: `./gradlew recoveryIntegrationTest --rerun --tests *RecoveryMigrationIT`, exit 0,
12/12 through Testcontainers (`final-gate-3-it-RecoveryMigrationIT.log`). `scripts/dev.ps1 up` was
not used.

| Surface | Status | Tests | Instruction | Branch | Line | Method |
|---|---|---|---|---|---|---|
| Backend | REQUIRED | 438 passed, 0 failed, 0 skipped (49 suites) | 90.91% (14257/15683) | 81.16% (1310/1614) | 91.14% (2623/2878) | 95.90% (561/585) |
| Frontend | NOT_APPLICABLE | N/A: no frontend file changed | N/A | N/A | N/A | N/A |

`recoveryCoverageReport.xml` in this folder is replaced by the round-3 report. Each counter is at or
above 0.80. Tests grew from 436 to 438: the two new lint fixtures (`RecoveryMigrationLintTest`
69 to 71).

Files changed in round 3: `LiteralSchemaRule.java` (test tooling), `RecoveryMigrationLintTest.java`,
the migration-folder `README.md`, and two new fixtures. No production Java, dependency, merged
migration or shared register changed; no personal data.

## Confirmation round 4 (CONF4-E044-01)

Input: `INC-001-epic-1-RWB-E1-044/review/code-gate-review-confirmation-4.md`,
`CODE_GATE: FAIL [C:0] [H:0] [M:0] [L:1]`, on `e15eaae`. No pattern case was added.

### CONF4-E044-01 (L): `$` inside a name is not a keyword boundary

- Fix: `\b` treats `$` as a word break, so the `on` in `idx$on` was taken for the object `ON`.
  `LiteralSchemaRule` now uses one boundary, `B`, in which `$` is a name character as in
  PostgreSQL, in place of every `\b` keyword boundary. That covers `ON_OBJECT` (both the `ON` search
  and the object `ON`) and the other position patterns (`POSITION`, `RULE_TO`, `COMMENT_ON`,
  `COMMENT_COLUMN`, `ADD_COLUMN`, `TABLE_OPEN`, `BARE_SCHEMA`). Around a keyword it is the reviewer's
  `(?<![\w$])ON(?![\w$])`.
- Fixture: `t02-on-dollar-name-fail` (failing): `CREATE INDEX idx$on ON rwb_case.t1 (a)`,
  `CREATE TRIGGER trg$on AFTER INSERT ON rwb_case.t1 ...` and
  `CREATE POLICY p$on ON rwb_case.t1 USING (true)`, each reported as `rwb_case`.
  `t02-on-quoted-name-fail` (`"audit on insert"`) and `t02-join-alias-pass` (the JOIN probes) are
  unchanged and pass.
- Commits: `73c897c` red, `66d6fdb` green.
- Evidence: `conf4-01-red.log` (no finding for the fixture), `conf4-01-green.log`
  (`RecoveryMigrationLintTest` 72/72).
- Status: fixed. The migration-folder `README.md` states the boundary.

### Final gate run (round 4)

Command, in `backend` at `66d6fdb`:
`./gradlew test --rerun recoveryCoverageReport recoveryCoverageVerification`, exit 0
(`final-gate-4.log`); `recoveryCoverageVerification` executed in that run.
Integration: `./gradlew recoveryIntegrationTest --rerun --tests *RecoveryMigrationIT`, exit 0,
12/12 through Testcontainers (`final-gate-4-it-RecoveryMigrationIT.log`). `scripts/dev.ps1 up` was
not used.

| Surface | Status | Tests | Instruction | Branch | Line | Method |
|---|---|---|---|---|---|---|
| Backend | REQUIRED | 439 passed, 0 failed, 0 skipped (49 suites) | 90.92% (14259/15683) | 81.23% (1311/1614) | 91.17% (2624/2878) | 95.90% (561/585) |
| Frontend | NOT_APPLICABLE | N/A: no frontend file changed | N/A | N/A | N/A | N/A |

`recoveryCoverageReport.xml` in this folder is replaced by the round-4 report. Each counter is at or
above 0.80. Tests grew from 438 to 439: one new lint fixture.

Files changed in round 4: `LiteralSchemaRule.java` (test tooling), `RecoveryMigrationLintTest.java`,
the migration-folder `README.md`, and one new fixture. No production Java, dependency, merged
migration or shared register changed; no personal data.

STATUS: COMPLETE. GATE_REVIEW: PENDING_ORCHESTRATOR (re-gate as `code-gate-review-confirmation-5.md`).
NEXT_STEP: Orchestrator starts the round-5 re-gate of CONF4-E044-01.