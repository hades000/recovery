# Code gate review (confirmation round 5): RWB-E1-044

| Field | Value |
|---|---|
| Story | RWB-E1-044, run `INC-001-epic-1-RWB-E1-044` |
| Reviewer | Compliance Reviewer, code gate mode (Claude Opus 5.5), read only |
| Date | 19 Nov 2026 |
| Diff range | `e15eaae..8f1d8ce` (round 5 changes) within `develop-recovery...8f1d8ce`, branch `fix/REVIEW-001-e1-044-confirmation`, worktree `rwb-wt/REVIEW-001-E1-044` |
| Previous gate | `review/code-gate-review-confirmation-4.md`, FAIL 0C/0H/0M/1L (CONF4-E044-01) |
| Measured against | `specify/spec.md` SPEC-003, SPEC-007; AGENTS.md §3.10, §3.16, §4.5 |
| Rule | D-RUN-09: any finding, Low included, fails the gate. Churn rule: only real defects shown with a concrete input a realistic recovery migration could contain; a limitation the README states is not a finding |

## 1. What I ran

- `./gradlew test --rerun --tests *RecoveryMigrationLintTest*` in the worktree `backend` at `8f1d8ce` (with `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=...\.gradle\uds`): BUILD SUCCESSFUL, `RecoveryMigrationLintTest` 72 tests, 0 failed, 0 errors, 0 skipped. Working tree clean before and after.
- 45 probe migrations in my scratchpad (30 that must report, 15 that must not), linted end to end with `MigrationLint.lint` on the compiled classes through jshell. Every "must report" probe reported exactly the expected qualifier on the expected line; every "must not report" probe gave no `L-LITERAL-SCHEMA` finding.
- A differential check of the boundary change itself: for each of the eight changed patterns I read the compiled `Pattern` by reflection and built the round-4 form by replacing `B` with `\b` (the change was a one-for-one substitution; I confirmed `B` occurs in all eight). Both forms were run over 122 `.sql` files: every lint fixture, the merged `V0001__rwb_e1_042_parameter_catalog_and_seed.sql`, and my 45 probes. No repository file was changed.
- Not run: `dev.ps1 up`, `it`, `e2e`. Builder evidence read: `final-gate-4.log` (49 suites, 439 tests, 0 failed; 90.92% instruction, 81.23% branch, 91.17% line, 95.90% method; exit 0 at `66d6fdb`) and `final-gate-4-it-RecoveryMigrationIT.log` (12/12 through Testcontainers, exit 0).

## 2. Previous findings

| ID | Status | Evidence |
|---|---|---|
| CONF4-E044-01 | Closed | `B` = `(?:(?<![\w$])(?=[\w$])\|(?<=[\w$])(?![\w$]))`, `LiteralSchemaRule.java:38`, used in place of every `\b` in `POSITION`, `ON_OBJECT` (`:62-66`, both the `ON` search and the object `ON`), `RULE_TO`, `COMMENT_ON`, `COMMENT_COLUMN`, `ADD_COLUMN`, `TABLE_OPEN`, `BARE_SCHEMA`. Around a keyword `B ON B` is exactly `(?<![\w$])ON(?![\w$])`, the form the round-4 review proposed. Fixture `t02-on-dollar-name-fail` (`CREATE INDEX idx$on`, `CREATE TRIGGER trg$on`, `CREATE POLICY p$on`, each `ON rwb_case.t1`), expectation at `RecoveryMigrationLintTest.java:162`: three `rwb_case` findings on lines 2-4. The round-4 probes now report: `idx$on`, `trg$on`, `p$on`, plus `on$x` before `ON`, `DROP TRIGGER trg$on ON`, `ALTER RULE r$on ON`, `COMMENT ON TRIGGER trg$on ON`, and a multi-line `trg$on` / `AFTER INSERT` / `ON rwb_case.t1` (reported on the qualifier's line 4). `"audit on insert"` and the `CREATE POLICY ... JOIN ... ON a.id` probe are unchanged |

Red before green: `73c897c` (01:26:08 +0700) touches only `RecoveryMigrationLintTest.java`, the new fixture and `conf4-01-red.log`; `66d6fdb` (01:27:06) touches only `LiteralSchemaRule.java`, the README and `conf4-01-green.log`; `8f1d8ce` is evidence only. `conf4-01-red.log` shows the new fixture failing with 0 of 3 findings and the other 71 passing. No test was weakened or skipped.

The fixture fails without the fix and only through `ON_OBJECT` (AGENTS §3.16): in the differential run the round-4 `ON_OBJECT` gives no match on it, the new one gives the three `rwb_case` matches, and no other pattern (old or new) matches anything in that file. `rwb_case` is not a known schema, so `QUALIFIED` does not report it either. Removing the `ON_OBJECT` check turns the fixture red.

## 3. Regression check of the boundary change

Over the 122 files the old and new forms of all eight patterns gave identical matches everywhere except the following, all of which involve a `$` next to a keyword:

| Pattern | Input | Round 4 (`\b`) | Round 5 (`B`) | Effect on the lint |
|---|---|---|---|---|
| `ON_OBJECT` | `t02-on-dollar-name-fail`; probes `on$x`, `trg$on` (DROP TRIGGER, multi-line CREATE TRIGGER), `r$on` (ALTER RULE); `idx$on ON ${recoverySchema}.t1` | no match | match | The fix. The `${recoverySchema}` case is matched and then allowed, so it still gives no finding |
| `BARE_SCHEMA` | `CREATE TABLE ${recoverySchema}.t1 (x$schema int, ...)` | match, qualifier `int` | no match | A false positive in round 4 (`literal schema int`) is gone |
| `POSITION` | `AS $$UPDATE rwb_case.t1 ...$$`, `AS $fn$TRUNCATE rwb_case.t1$fn$` on raw text | match | no match on raw text | None. The lint runs on the identifier view, where `MigrationLexer` blanks dollar-quote delimiters (`MigrationLexer.java:233-234`), so the keyword follows a space. Both probes report `rwb_case` end to end, as does `DO $$BEGIN UPDATE rwb_case.t1 ...$$` |

`$` is left in the identifier view only inside names (`dollarTagLength` refuses a `$` that continues an identifier, `MigrationLexer.java:395`), in `${...}` placeholders (which end with `}`, a non-name character) and in positional parameters such as `$1` (`SELECT $1::rwb_case.ty1` still reports through `::`, which has no boundary). I found no realistic input where `B` drops a finding `\b` gave or adds a false positive. Probes per pattern that still report: `POSITION` (`TABLE`, `FROM`, `INTO`, `OWNED BY`, `::`, `UPDATE`/`TRUNCATE` in a dollar body), `ON_OBJECT` (`UNIQUE INDEX`, `ON ONLY`, `idx_on`, `GRANT`, `REVOKE`, quoted policy name), `RULE_TO` (`r$x`), `COMMENT_ON` (`INDEX`, `TRIGGER ... ON`), `COMMENT_COLUMN` (`s.t.c`), `ADD_COLUMN` (`ADD COLUMN c`, `ADD c$x`), `TABLE_OPEN`/`COLUMN_TYPE` (`numeric(18, 2)` then `b rwb_case.ty1`, `t$1 (a$b rwb_case.ty1)`), `BARE_SCHEMA` (`CREATE SCHEMA`, `IN SCHEMA`). Probes that still pass: join `ON t1.id`, the policy join, `COMMENT ON COLUMN t1.a`, `ADD COLUMN c pg_catalog.int4`, `ADD CONSTRAINT ... CHECK`, `CHECK (a > 0)` in a column list, `ON SCHEMA ${recoverySchema}`, `RULE ... TO ${recoverySchema}.t1`, `a$from` and `v$as` aliases, a partial index with `USING btree ... WHERE`.

## 4. New findings

None.

## 5. Other checks

| Check | Result | Notes |
|---|---|---|
| Unit tests | PASS | Lint suite 72/0/0/0 on my `--rerun`; full suite 439/0/0/0 in `final-gate-4.log` |
| Red before green | PASS | `73c897c` before `66d6fdb`; the red log fails exactly the new fixture |
| Each new fixture fails without its fix | PASS | Shown by `conf4-01-red.log` and by the differential: only `ON_OBJECT` matches the fixture |
| Tests weakened or skipped | PASS | One expectation added, none changed; no `@Disabled` |
| False positives on `V0001` and pass fixtures | PASS | All green; old and new patterns match identically on the merged migration and every pass fixture |
| Regular-expression cost | PASS | The lint suite (72 tests) ran in 0.38 s on my `--rerun`; the lookarounds in `B` add constant work per character |
| README and report match the code | PASS | `README.md:61-64` ("a keyword boundary treats `$` as part of a name ... in `CREATE INDEX idx$on ON s.t` the name `idx$on` holds no keyword and `s` is checked") matches the code and my probes. The implementation report's CONF4 section names the eight patterns that use `B`, which matches the diff, and its statement that `B` around a keyword equals `(?<![\w$])ON(?![\w$])` is correct |
| Dependencies, merged migrations, production code | PASS | Only test tooling, one test fixture, the migration-folder README and evidence changed |
| PII and literals | PASS | Synthetic names only |
| Coverage | PASS | Backend 90.92% instruction, 81.23% branch, 91.17% line, 95.90% method (builder `final-gate-4.log`). Frontend NOT_APPLICABLE |
| Commit trailers (AGENTS §4.12) | PASS | All three commits carry `Co-Authored-By: Claude Opus 5.5` and the AISDLC trailers |

REVIEW_TYPE: CODE_GATE_REVIEW (CONFIRMATION ROUND 5)
CODE_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
