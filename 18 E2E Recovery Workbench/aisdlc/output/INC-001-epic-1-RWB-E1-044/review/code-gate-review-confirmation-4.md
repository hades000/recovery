# Code gate review (confirmation round 4): RWB-E1-044

| Field | Value |
|---|---|
| Story | RWB-E1-044, run `INC-001-epic-1-RWB-E1-044` |
| Reviewer | Compliance Reviewer, code gate mode (Claude Opus 5.5), read only |
| Date | 19 Nov 2026 |
| Diff range | `f319748..e15eaae` (round 4 changes) within `develop-recovery...e15eaae`, branch `fix/REVIEW-001-e1-044-confirmation`, base `27567ed`, worktree `rwb-wt/REVIEW-001-E1-044` |
| Previous gate | `review/code-gate-review-confirmation-3.md`, FAIL 0C/0H/0M/3L (CONF3-E044-01..03) |
| Measured against | `specify/spec.md` SPEC-003, SPEC-007; AGENTS.md §3.10, §3.16, §4.5 |
| Rule | D-RUN-09: any finding, Low included, fails the gate. Churn rule: only real defects shown with a concrete input; a limitation the README states is not a finding |

## 1. What I ran

- `./gradlew test --tests *RecoveryMigrationLintTest* --rerun` in the worktree `backend` at `e15eaae` (with `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=...\.gradle\uds`): BUILD SUCCESSFUL, `RecoveryMigrationLintTest` 71 tests, 0 failed, 0 errors, 0 skipped. Working tree clean before and after.
- 16 probe migrations in my scratchpad, linted with `MigrationLint.lint` on the compiled classes through jshell; then the current `ON_OBJECT` pattern compared with a candidate fix on five of them. No repository file was changed.
- Not run: `dev.ps1 up`, `it`, `e2e`. Builder evidence read: `final-gate-3.log` (49 suites, 438 tests, 0 failed; 90.91% instruction, 81.16% branch, 91.14% line, 95.90% method; exit 0 at `c94e183`) and `final-gate-3-it-RecoveryMigrationIT.log` (12/12 through Testcontainers, exit 0).

## 2. Previous findings

| ID | Status | Evidence |
|---|---|---|
| CONF3-E044-01 | Closed for quoted identifiers; the same root cause remains for an unquoted name, see CONF4-E044-01 | `ON_OBJECT` token `(?:"(?:[^"]\|"")*"\|(?!\bON\b)[^;"])*`, `LiteralSchemaRule.java:56-59`. Fixture `t02-on-quoted-name-fail` (both lines `rwb_case`), `RecoveryMigrationLintTest.java:160`. Red `05af35d` before green `c94e183`; `conf3-01-02-red.log` shows the fixture with 0 of 2 findings, `conf3-01-02-green.log` 71/71. Without the fix the old token stops at `on` inside the quotes and nothing else reports `rwb_case` (not a known schema, no `POSITION` keyword), so the fixture is red only through this check (AGENTS §3.16). Probes reported: `"a""on""b"`, `"x;on"`, `U&"on"`; `GRANT SELECT ("on") ON rwb_case.t1`. Probes passing: `EXECUTE FUNCTION "on"()` on an unqualified table, the `CREATE POLICY ... JOIN ... ON a.id` join |
| CONF3-E044-02 | Closed | `RULE_TO`, `LiteralSchemaRule.java:64-66`, collected at line 111. Fixture `t02-create-rule-to-fail` (`CREATE OR REPLACE RULE ... ON INSERT TO rwb_case.t1`, `CREATE RULE ... ON UPDATE TO rwb_case.t2`), `RecoveryMigrationLintTest.java:161`. Red `05af35d` (0 of 2 findings) before green `c94e183`. No broader check reports either line: `CREATE RULE` is not an `ON_OBJECT` prefix, `TO` is not a `POSITION` keyword, `rwb_case` is not a known schema. Probes reported: quoted rule name `"r on x"`, multi-line `AS / ON SELECT / TO` (reported on the qualifier's line 4), comments and `rwb_case . t1` spacing. Probes passing: `TO ${recoverySchema}.t1`, an unqualified `TO t1 WHERE EXISTS (... JOIN ... ON a.id = b.id)` |
| CONF3-E044-03 | Closed (claim narrowed, no code) | `README.md:63-65`: "`COMMENT ON <kind>` is checked for every kind except `CAST`", source type stated as a known limitation, target type after `AS` checked. Implementation report CONF2-E044-01 status and CONF3-E044-03 section say the same. Probes match the text exactly: `COMMENT ON CAST (rwb_case.ty1 AS int)` gives no finding; `COMMENT ON CAST (int AS rwb_case.ty2)` reports `rwb_case` |

Red before green: `05af35d` (01:17:15 +0700) touches only `RecoveryMigrationLintTest.java`, the two fixtures and the red log; `c94e183` (01:17:46) touches only `LiteralSchemaRule.java`, the README and the green log; `e15eaae` is evidence only. No test was weakened or skipped.

## 3. New findings

| ID | Severity | Where | Defect | Required fix |
|---|---|---|---|---|
| CONF4-E044-01 | Low | `LiteralSchemaRule.java:58` (`(?!\bON\b)[^;"]`, rewritten in `c94e183`); `README.md:59-62` | Same root cause as CONF3-E044-01, now for an unquoted name. PostgreSQL allows `$` after the first character of an identifier (the lint's own `QUALIFIER` and `NAME` accept `[A-Za-z0-9_$]`, and SPEC-007 says a `$` may continue an identifier), but `\b` treats `$` as a non-word character. So in `idx$on` the token stops at `on`, `ON\s+` then reads `ON` as the qualifier, finds no dot, and the whole match fails. At `e15eaae` each of these gives no finding: `CREATE INDEX idx$on ON rwb_case.t1 (a);`, `CREATE TRIGGER trg$on AFTER INSERT ON rwb_case.t1 FOR EACH ROW EXECUTE FUNCTION f1();`, `CREATE POLICY p$on ON rwb_case.t1 USING (true);`. The pre-round-2 pattern at `a241338` (`[^;]*?\bON\s+...`) reported all three, so this is a false negative introduced by `4af496b` and kept by the round-4 rewrite. The README says the checked `ON` is "the first `ON` after ... which is the object name"; the `on` inside `idx$on` is not | Use an identifier-aware boundary for `ON` in the token and before the object name, for example `(?!(?<![\w$])ON(?![\w$]))[^;"]` and `(?<![\w$])ON\s+`. With that change I measured all three probes reported as `rwb_case`, `"audit on insert"` still reported, and the `CREATE POLICY ... JOIN ... ON a.id` probe still passing. Add one probe line, qualifier `rwb_case`, to a failing fixture (for example `t02-on-quoted-name-fail`), red before green. Or state the `$` case as a known limitation in the README |

## 4. Other checks

| Check | Result | Notes |
|---|---|---|
| Unit tests | PASS | Lint suite 71/0/0/0 on my `--rerun`; full suite 438/0/0/0 in `final-gate-3.log` |
| Red before green | PASS | `05af35d` before `c94e183`, red log fails exactly the two new fixtures |
| Each new fixture fails without its fix | PASS | Shown by `conf3-01-02-red.log` (0 of 2 findings in each) and by the code: no other pattern reports `rwb_case` on those lines |
| Tests weakened or skipped | PASS | Two expectations added, none changed; no `@Disabled` |
| False positives on `V0001` and pass fixtures | PASS | All green; join probes inside `CREATE POLICY` and `CREATE RULE ... WHERE` pass |
| Regular-expression cost | PASS | The new nested quantifier on quoted identifiers did not slow the lint: an index name with 16, 20 and 22 escaped `""` pairs linted in 31 ms or less |
| README and report match the code | FAIL, see CONF4-E044-01 | The `TO`, quoted-identifier and `CAST` statements match the code exactly; the "first `ON` ... which is the object name" statement does not hold for a `$`-name |
| Dependencies, merged migrations, production code | PASS | Only test tooling, test fixtures, the migration-folder README and evidence changed |
| PII and literals | PASS | Synthetic names only |
| Coverage | PASS | Backend 90.91% instruction, 81.16% branch, 91.14% line, 95.90% method (builder `final-gate-3.log`). Frontend NOT_APPLICABLE |
| Commit trailers (AGENTS §4.12) | PASS | All three commits carry `Co-Authored-By: Claude Opus 5.5` and the AISDLC trailers |

REVIEW_TYPE: CODE_GATE_REVIEW (CONFIRMATION ROUND 4)
CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 1]
