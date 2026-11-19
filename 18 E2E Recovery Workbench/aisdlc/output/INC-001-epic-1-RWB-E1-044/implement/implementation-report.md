# Implementation report: RWB-E1-044

Run `INC-001-epic-1-RWB-E1-044`, stage `implement`, including the pre-merge review fix round.
Worktree `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-E1-044`,
branch `feature/RWB-E1-044-db-migrations`, base `f36991a` (RWB-TE-001 merged).

## Commits

| SHA | Content |
|---|---|
| `ed4f496` | One-pass migration tokenizer and parsed file model |
| `42eb802` | Migration lint rules, registry and fixture corpus |
| `98e661e` | Schema snapshot reader and pure drift comparator |
| `b3bc5ce` | Pin `rwb.schema` to `recovery` at properties binding |
| `e8581b4` | Migration failure reported as MSG-P3-016 and `validateOnMigrate(true)` |
| `a9400ed` | Container proof of Flyway behaviour and the D-RUN-14 migrator rights |
| `1ac16c0` | Coverage wiring, README conventions and story files |
| `c253b3c` | **Pre-merge review fixes** (first round) |
| `a74324a` | **Round 2 review fixes**: dynamic-GRANT precision, size pre-check before read, correct block-comment matching |
| `42083a4` | **Round 3 review fixes**: robust `EXECUTE` argument literal analysis (dollar, `format(...)`, concatenation) |
| `d00235f` | **Round 4 review fixes**: L-GRANT simplified to a dynamic statement-start check |
| `1cfe5f1` | **Round 5**: L-GRANT restored to SPEC-009; dynamic-SQL gap DG-E044-DYN-01 recorded |
| `89477bc` | **Code-gate fix**: SPEC-016 seam statement mapped by offset range (CODE-001); evidence corrected (CODE-002, CODE-003) |

## Pre-merge review fix

Reviews: `review/ponytail-review.md` (tip `1ac16c0`) and `review/security-review.md`
(0 Critical / 0 High / 0 Medium / 4 Low / 1 Info). Every finding is fixed in `c253b3c`.

| Finding | Fix | Fails-before / passes-after test | Evidence |
|---|---|---|---|
| Ponytail Must 1, Security Low 4 (`SEC-044-04`) | `RecoveryMigrationRunner.failureObject` wraps the whole detail lookup in `try/catch RuntimeException` and returns `recoveryFlyway`; null/blank invalid versions are skipped and `display` no longer parses an empty part. The original exception is always logged once and rethrown. | `RecoveryMigrationRunnerTest`: `aDetailLookupFailureStillLogsTheFallbackAndRethrowsTheOriginal` (`info()` throws), `anInvalidVersionThatIsBlankFallsBackInsteadOfFailing` (repeatable's empty version), `aBrokenConnectionStillLogsTheFallbackAndRethrows` (a real Flyway against a closed port, not a mocked `info()`) | `review-fix/red-unit.log`, `review-fix/green-unit.log` |
| Ponytail Must 2 | `SequenceGapRule` reports `L-SEQ-GAP` when the lowest sequence is below the first, in addition to the gap check. | `t01-seqzero-fail` (`V0000`) | `review-fix/red-unit.log`, `green-unit.log` |
| Ponytail Should 3, Security Low 1 (`SEC-044-01`) | `MigrationLint.lint` no longer returns empty for a missing folder; `Files.list` fails closed with an `UncheckedIOException` naming the folder. | `RecoveryMigrationLintTest.aMissingFolderFailsClosed` | `red-unit.log`, `green-unit.log` |
| Ponytail Should 4 | `SchemaSnapshotReader.read` reads `pg_catalog.format_type(atttypid, atttypmod)` and `attnotnull`, so length, precision/scale and enum types are compared; unit cases added. | `driftComparisonSeesAColumnLengthChange` (`varchar(8)` vs `varchar(50)`), plus three comparator cases | `review-fix/red-drift-type.log`, `review-fix/it.log` |
| Ponytail Should 5 | `SchemaSnapshotReader.read(Connection, String, String historyTable)` takes the name; `RecoveryMigrationIT` passes `RecoveryFlywayConfig.HISTORY_TABLE` and derives `HISTORY` from it for its SQL. One constant, no literal in tooling. | IT green | `review-fix/it.log` |
| Security Low 2 (`SEC-044-02`) | `L-LITERAL-SCHEMA` and `L-FK-OUTSIDE` run their patterns over the whole identifier text and derive the line from the match, so whitespace, a newline or a comment before the dot no longer hides the reference. | `t21-split-qualifier-fail`, `t05-fk-split-fail` | `red-unit.log`, `green-unit.log` |
| Security Low 3 (`SEC-044-03`) | `L-GRANT` also fails a `DO` statement or any `EXECUTE` statement whose text contains GRANT/REVOKE (dynamic SQL). | `t20-grant-fail` lines 5 and 6 | `red-unit.log`, `green-unit.log` |
| Security Info (`SEC-044-05`) | 262144-character cap, dollar-quote nesting cap 32, a memo for an unterminated block comment (removes the quadratic rescan) and precomputed line starts (binary search). Clear `IllegalArgumentException` messages. | `MigrationLexerTest`: `aFileAtTheSizeLimitParsesAndOneCharacterMoreFailsClosed`, `repeatedUnterminatedBlockCommentsStayLinear` (200 KB within 5 s), `deeplyNestedDollarBodiesFailClosedAtTheBound`, `aSmallDollarNestingDepthIsAccepted` | `red-unit.log`, `green-unit.log` |
| Ponytail Nice 6 | `HeaderMultiRule` strips leading whitespace before matching `-- Story:`. | `t03-header-multi-indented-fail` | `red-unit.log`, `green-unit.log` |
| Ponytail Nice 7 | Deleted `SchemaComparator.format` and `SchemaDifference.toString`; the test calls `difference.format()`. | `SchemaComparatorTest` compiles and passes | `green-unit.log` |

The README (`db/modulemigration/recovery/README.md`) now states the start-at-first-sequence rule,
the dynamic-SQL grant rule and the input bounds.

### Round 2 (ponytail closure check on `c253b3c`)

| Finding | Fix | Test |
|---|---|---|
| New 8 (Should) | `L-GRANT` now flags only an `EXECUTE` string literal whose content starts with GRANT/REVOKE after whitespace; a quoted column `"execute"` or `"grant"` is an identifier and no longer produces a finding. `t20-grant-fail` still gives its five findings. | new passing fixture `t20-grant-quoted-pass` (`"execute" text, "grant" text`); red before, green after |
| Info (security) | `MigrationLexer.parse(Path)` checks `Files.size` before `Files.readString`, so an over-limit file fails with the size message without being read. | `anOverLimitFileFailsOnItsSizeBeforeItIsRead` (262145 bytes of invalid UTF-8; red threw `MalformedInputException`, green throws `IllegalArgumentException`) |
| Info (security) | Block-comment ends are computed once with a stack (`/*`/`*/` pairing) instead of the unsound failure memo, so `/* /* */` gives exactly one `L-LEX` and a later opener still closes; the repeated-`/*` file stays linear. | `anUnterminatedNestedBlockCommentIsReportedOnce` plus the existing 200 KB linearity test |

Round-2 evidence: `implement/review-fix/round2/red.log`, `green-targeted.log`,
`unit-coverage.log`, `counters.txt`, `recoveryCoverageReport.xml`. The container suite is unchanged
by this round (test-scope only) and was last green at `c253b3c` (18/18).

### Round 3 (ponytail closure check on `a74324a`)

The narrowed `EXECUTE`-literal check missed three forms that can execute GRANT: a dollar-quoted
argument, a literal inside `format(...)`, and a literal after a concatenation.

`GrantRule` now walks the `EXECUTE` argument and inspects **every** literal after the keyword:
single-quoted (including `''` and `E'…'` escapes), dollar-quoted (`$tag$…$tag$`, descending into the
body so a `DO` block's inner `EXECUTE` is found), and literals nested in `format(...)` or
concatenations. A literal that contains GRANT or REVOKE as a word fails. Double-quoted identifiers
and bare identifiers are skipped, so `"execute"`/`"grant"` never match; an unresolvable expression is
not guessed at.

| Fixture | Form | Expected |
|---|---|---|
| `t20-grant-dollar-fail` | `EXECUTE $q$GRANT …$q$` | one `L-GRANT` at :2 |
| `t20-grant-format-fail` | `EXECUTE format('GRANT …')` | one `L-GRANT` at :2 |
| `t20-grant-concat-fail` | `EXECUTE 'SELECT 1; ' \|\| 'GRANT …'` | one `L-GRANT` at :2 |
| `t20-grant-identifiers-pass` | word only in double-quoted identifiers, a comment, a non-EXECUTE literal and a bare identifier | none |

`t20-grant-fail` keeps its six findings (an `E'…'` line is added); `t20-grant-quoted-pass` stays
green.

Round-3 evidence: `implement/review-fix/round3/red.log`, `green-targeted.log`,
`unit-coverage.log`, `counters.txt`, `recoveryCoverageReport.xml`.

### Round 4 (ponytail closure check on `42083a4`, finding 11) - **superseded by round 5**

The dynamic-SQL analysis described below is beyond SPEC-009 and was removed in round 5; the rule is
the spec's line-start/statement-start check. The text is kept only as the review history.

Round 3 scanned the whole literal, so a GRANT word in a notice, column alias or comment-like text
false-positived, and the `afterExecute` state leaked across `;`. The rule is now the small,
statement-start check the run-book churn rule asks for:

1. Each `EXECUTE` keyword is found outside literals and identifiers; its argument is reduced on the
   spot (no persistent `afterExecute` state, so a later `RAISE NOTICE`, `SELECT` or comment literal
   never inherits it).
2. Literal operands are concatenated across `||`: single-quoted, `E'…'`, dollar-quoted, and
   `format('…')` (its literals are collected).
3. The resulting dynamic text is split on `;`, leading whitespace and SQL comments are stripped, and
   only a first keyword of GRANT or REVOKE fails.
4. A word later in the dynamic statement, a quoted identifier, a comment or a literal outside an
   EXECUTE argument does not fail.

Fixtures: must-fail `t20-grant-fail` (six findings), `t20-grant-dollar-fail`,
`t20-grant-format-fail`, `t20-grant-concat-fail`; must-pass `t20-grant-quoted-pass`,
`t20-grant-identifiers-pass`, `t20-grant-mid-text-pass` (`EXECUTE 'SELECT ''GRANT failed'''`),
`t20-grant-raise-pass` (`EXECUTE 'SELECT 1'; RAISE NOTICE 'GRANT failed'`) and
`t20-grant-column-pass` (`SELECT execute, 'GRANT failed'`). All green.

**Named residual RES-E044-01.** When the `EXECUTE` argument is a bare identifier, function or
parameter (`EXECUTE v_sql;`, `EXECUTE grant_proc;`) the text cannot be resolved. The rule does not
guess; code review and the database grants remain the control. Recorded here and in the migration
README, not represented as a passing test.

Round-4 evidence: `implement/review-fix/round4/red.log`, `green-targeted.log`,
`unit-coverage.log`, `counters.txt`, `recoveryCoverageReport.xml`.

### Round 5 (spec-scope correction on `d00235f`)

The gated SPEC-RWB-E1-044-009 defines `L-GRANT` exactly: "fails when GRANT or REVOKE is the first
word of a line (inherited) or of a statement (new, so `SELECT 1; GRANT ...` on one line is caught).
The statement's first word is read as SPEC-007 view (c) states, so a leading comment never hides or
supplies it." T-044-20 covers the line-start, statement-start, `-- GRANT` and `/* REVOKE */` cases.
The dynamic-SQL analysis added in rounds 3 and 4 is beyond that definition.

- `GrantRule` is restored to the spec exactly: the identifier-view statements supply the first word
  and start line, the code-text lines supply the line-start check, and no `EXECUTE`, literal,
  dollar-quote, `format` or concatenation scanning remains.
- Out-of-spec fixtures removed: `t20-grant-dollar-fail`, `t20-grant-format-fail`,
  `t20-grant-concat-fail`, `t20-grant-mid-text-pass`, `t20-grant-raise-pass`,
  `t20-grant-column-pass`, `t20-grant-identifiers-pass`.
- Kept, and consistent with SPEC-009: `t20-grant-fail` (GRANT and REVOKE at line start, and
  `SELECT 1; GRANT …` at statement start), `t20-grant-pass` (`-- GRANT` and `/* REVOKE */` pass) and
  `t20-grant-quoted-pass` (quoted identifiers are not a statement start).
- **Gap `DG-E044-DYN-01`** recorded in `implement/document-gaps.md`: SPEC-009 does not inspect
  GRANT/REVOKE inside `EXECUTE`/`DO` dynamic SQL (security review SEC-044-03, Low). Blocker = No. The
  rule follows the spec; a future `L-DYNAMIC-SQL` rule or a documented ban on dynamic SQL in
  migrations is suggested, owned by the recovery tech lead / specification owner. It is recorded, not
  silently accepted.
- RES-E044-01 is withdrawn with the dynamic analysis it described; the residual is now the gap row.

Round-5 evidence: `implement/review-fix/round5/unit-coverage.log`, `counters.txt`,
`recoveryCoverageReport.xml`.

### Code-gate fix (three Lows on `1cfe5f1`)

| Finding | Fix |
|---|---|
| CODE-001 (Low, real) | `LiteralSchemaRule.statementAt` now finds the statement whose identifier-view `[startOffset, endOffset)` contains the qualifier, not one whose start line matches. The SPEC-016 seam (`isAllowedQualifier`) therefore receives the statement for a qualifier on a later line of a multi-line statement; no rule result changes. |
| CODE-002 (Low, evidence) | `implement/unit-tests/report.md` headline replaced with the final run (243 tests, 27 classes), the round-5 snapshot (242 tests, LINE 94.86 / INSTRUCTION 94.28 / BRANCH 86.26 / METHOD 97.98) cited to `review-fix/round5/`, and the first-round 226-test snapshot labelled pre-fix. |
| CODE-003 (Low, evidence) | `implement/deviations.md` DEV-E044-01 corrected to 18 integration tests (12 `RecoveryMigrationIT` + 6 `RecoveryDatabaseIT`). |

New test `LiteralSchemaRuleTest.aQualifierOnALaterLineOfAMultiLineStatementFindsItsStatement`:
a three-line `CREATE TABLE` whose `REFERENCES public.t1(id)` sits on line 3. Against the previous
start-line lookup the seam received `null` (red, `implement/code-gate-fix/red-statement-range.log`);
after the offset-range fix it receives the statement (green).

Code-gate evidence: `implement/code-gate-fix/red-statement-range.log`, `green-targeted.log`,
`unit-coverage.log`. Tip `89477bc`; unit 243 tests, 0 failed/skipped; coverage LINE 0.9481 /
INSTRUCTION 0.9426 / BRANCH 0.8607 / METHOD 0.9798, `test recoveryCoverageVerification` exit 0. Tip `1cfe5f1`; unit 242 tests, 0 failed/skipped; coverage LINE 0.9486 /
INSTRUCTION 0.9428 / BRANCH 0.8626 / METHOD 0.9798, `test recoveryCoverageVerification` exit 0.

## Unit test results (after the review fix)

| Surface | Passed | Failed | Skipped | Statements % | Branches % | Functions % | Lines % | Required % | Status | Evidence |
|---------|--------|--------|---------|--------------|------------|-------------|---------|------------|--------|----------|
| Backend (main + test-scope tooling) | 243 | 0 | 0 | 94.26 | 86.07 | 97.98 | 94.81 | 80 | PASS | `code-gate-fix/unit-coverage.log`; coverage XML from the same run; round-5 snapshot in `review-fix/round5/` |
| Frontend | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | NOT_APPLICABLE | UI In Scope NO; no `frontend/` change; `npm run check` was green in the first round and no frontend file changed in this round |

Container (`./gradlew recoveryIntegrationTest`): 18 passed (12 `RecoveryMigrationIT` + 6
`RecoveryDatabaseIT`), 0 failed, 0 skipped, exit 0 - `review-fix/it.log`.

## Status lines

```text
IMPLEMENT_MCP_STATUS_SUMMARY: RWB-E1-044 code-gate Lows are fixed: the SPEC-016 seam maps the statement by offset range, evidence counts/counters corrected; unit 243/243, coverage 0.9481/0.9426/0.8607/0.9798.
IMPLEMENT_MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
IMPLEMENT_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO; DESIGN_EVIDENCE_STATUS NOT_REQUIRED]
UI_FIDELITY_SUMMARY: Not applicable: the story adds no screen, route or component; SCR-44 is out of scope (D-RCV-12).
UI_FIDELITY_RESULT: NOT_APPLICABLE [TOTAL_NODES: 0] [MATCHED_NODES: 0] [MISSING_NODE_ARTIFACTS: 0] [STYLE_MISMATCHES: 0] [TEXT_MISMATCHES: 0] [CONTRADICTIONS: 0]
GATE_REVIEW: PENDING_ORCHESTRATOR
```

## Handoff

All pre-merge review findings are fixed and green. The branch is not merged. Deviations from the
first round are in `deviations.md`; this round adds no deviation. No shared file was edited.
