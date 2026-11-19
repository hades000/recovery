# Code gate review: RWB-E1-044

> Orchestrator note (19 Nov 2026, REVIEW-001 H-10): the round 1 verdict below ("PASS_WITH_WARNINGS ... The Low
> findings do not block") is the reviewer's own text. Under D-RUN-09 the orchestrator did not accept it; the three
> Lows were fixed and round 2 in this same file passed with 0 findings. This file holds both rounds.
> A Claude Opus 5.5 confirmation gate on the merged code is in `code-gate-review-confirmation.md` (D-RUN-26).

**Run:** `INC-001-epic-1-RWB-E1-044`
**Story:** RWB-E1-044 Database migrations versioned with parameterized schema names
**Branch / tip / base:** `feature/RWB-E1-044-db-migrations` @ `1cfe5f1`; base `develop-recovery` @ `f36991a`
(RWB-TE-001 merged, D-RUN-17). Merge-base is `f36991a`.
**Reviewer:** `compliance-reviewer` (code gate)
**Date:** 18 November 2026
**Scope:** full diff `git diff develop-recovery...feature/RWB-E1-044-db-migrations`, 126 files,
4043 insertions, 96 deletions.

## Verdict

`PASS_WITH_WARNINGS` - 0 Critical / 0 High / 0 Medium / 3 Low. The Low findings do not block.
No `AGENTS.md` section 9 sign-off is recorded; OPEN-016 remains open.

## Inputs checked independently

- Spec v14-7 (`specify/spec.md`), spec gate round 7 PASS (0/0/0/0); 28 requirement-logic rows,
  AC1-AC9 and BR1-BR8.
- Plan v2 (`plan/plan.md`), plan gate round 2 PASS (0/0/0/0); 20 tasks TASK-00..TASK-19 and
  `implement/code-map.md` CODE-E044-001..031.
- Implementation report, `implement/review-fix/round5/` counters and JaCoCo XML, the Gradle test
  results, `implement/review-fix/it.log`, `review/security-review.md`, `review/ponytail-review.md`,
  `implement/scope-check.md`, `implement/deviations.md` and `implement/document-gaps.md`.
- D-RUN-07 (no production migration), D-RUN-14 (migrator rights), D-RUN-17 (TE-001 first),
  D-RUN-21 (one module).

## Findings

| ID | Severity | Area | Finding | Evidence | Required action |
|---|---|---|---|---|---|
| CODE-001 | Low | SPEC-016 extension point | `LiteralSchemaRule.statementAt` selects a statement only when `statement.startLine() == line`. A qualifier on a later line of a multi-line statement (the normal shape of `CREATE VIEW ... AS SELECT ... FROM public...`) is passed to `isAllowedQualifier` as `null`. No current rule result changes, because the three allowed names never consult the statement, but the SPEC-016 seam contract ("It gets the whole statement, so a later rule can depend on the statement kind") is not met for SEAM-E044-01. | `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/rule/LiteralSchemaRule.java:75,83-84`; seam fixture `t02-seam-marker-fail` is single-line; no multi-line seam test | Select the enclosing statement by offset (`startOffset <= matchOffset <= endOffset`) and add one multi-line seam-readiness test. Fix before RWB-E1-069 relies on the seam; not a current AC failure. |
| CODE-002 | Low | Unit-test evidence | `implement/unit-tests/report.md` still records the first-round run: 239 tests and 94.27 statements / 86.30 branches / 97.98 functions / 94.88 lines. The final suite is 242 tests (26 suites, 0 failed, 0 skipped) and the round-5 counters are 94.28 instruction / 94.86 line / 86.26 branch / 97.98 method. The implementation report and the native XML are correct; the required unit-test evidence file is stale. | `implement/unit-tests/report.md` table vs `implement/review-fix/round5/counters.txt` and `recoveryCoverageReport.xml`; `backend/build/test-results/test` = 242 tests | Refresh `report.md` from the final run. No metric fails, so this is not blocking. |
| CODE-003 | Low | Review trail | `review/ponytail-review.md` is the round-1 review at tip `1ac16c0` and ends "Verdict: fix 1 and 2 first"; it holds no final Ship verdict or closure record. `implement/deviations.md` says 17 container tests where the final report and suite are 18 (12 `RecoveryMigrationIT` + 6 `RecoveryDatabaseIT`). The code fixes themselves are present and tested, but the review artifact is stale. | `review/ponytail-review.md` (44 lines, no closure); `implement/deviations.md` DEV-E044-01; `implement/review-fix/it.log` | Record the final review disposition in the review artifact, or state on the PR that the implementation report is the closure record. Not a code defect. |

## Gate checklist

| Gate | Result | Evidence |
|---|---|---|
| Spec and AC trace | PASS | Spec v14-7 gate PASS 0/0/0/0; 28/28 rows covered, AC1-AC9 and BR1-BR8 mapped; no unresolved contradiction (8 settled, DG-L01/DG-L09/DG-L11/DG-L12/DG-L13 etc.) |
| Plan, tasks and code trace | PASS | Plan v2 gate PASS; TASK-00..-19, CODE-E044-001..031; every SPEC 001-017 has a task and a test; no orphan |
| No skipped or weakened test | PASS | No `@Disabled`, `@Ignore` or `assume`; fixtures assert the complete finding list; the only TE-001 test change is the allowed `MigrationPropertiesConfig` addition, with no assertion changed |
| Unit gate, 80% x4 | PASS | 242 passed, 0 failed, 0 skipped; LINE 0.9486, INSTRUCTION 0.9428, BRANCH 0.8626, METHOD 0.9798 from the native `recoveryCoverageReport.xml`; `test recoveryCoverageVerification` exit 0 |
| Container suite | PASS | 18 passed (12 `RecoveryMigrationIT` + 6 `RecoveryDatabaseIT`), 0 failed, 0 skipped, `it.log` BUILD SUCCESSFUL; no skip without Docker |
| No new dependency | PASS | `backend/build.gradle.kts` diff is the `migrationToolingClasses` collection and the two JaCoCo task class-directory sets only; no dependency block changed |
| No PII, credential or secret | PASS | Synthetic fixture names and container passwords; the MSG-P3-016 line carries the ID and two parameters only; no credential in code, config, fixture or log |
| No direct ACE `public` read | PASS | New production code has no SQL; test-scope `SchemaSnapshotReader` reads `information_schema`/`pg_catalog` for `recovery`; `public.account` is a negative test only; T-044-17(d) proves zero table privilege |
| D-RUN-07 / no merged-migration edit | PASS | No `.sql` in `db/modulemigration/recovery` (README only); no migration file in the diff; every `V<seq>` file is a test fixture; README uses `V<seq>` with no fixed number |
| D-RUN-14 grants exactly | PASS | `20-grants.sql.inc` adds `GRANT USAGE ON SCHEMA public TO rwb_migrator;` and `GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE;` after the PUBLIC revoke; no table privilege, no CREATE, no ADMIN; role comments updated; T-044-17(a)-(f) |
| SPEC-009 GRANT/REVOKE | PASS | `GrantRule` fails GRANT/REVOKE as the first word of a line (code text) or a statement (identifier text); `t20-grant-fail` lines 2-4, `t20-grant-pass` (`-- GRANT`, `/* REVOKE */`) and `t20-grant-quoted-pass`; dynamic SQL is the recorded gap, not a claimed pass |
| SPEC-010 testability and fixtures | PASS | Folder in, findings out; every rule has failing and passing fixtures; production README-only folder green; rule, file, line and key asserted; non-`.sql` and unreadable entries fail closed |
| SPEC-016 lint structure | PASS with CODE-001 | Tooling package, one `MigrationRule` per rule ID, one ordered registry of 15, one `isAllowedQualifier`, no `public` exception; `ForeignKeyOutsideRule` never calls it; the seam marker still fails; statement resolution is the Low observation |
| `rwb.schema` pin with Flyway on and off | PASS | Unconditional `MigrationPropertiesConfig`; `@Validated`, `@NotNull` and `@Pattern(regexp = "recovery")` on `schema`; T-044-08 cases (1)-(6) cover wrong/blank, relaxed `RWB_SCHEMA`, Flyway false/true and direct construction; error is a bind failure, not a Flyway failure |
| `DG-E044-DYN-01` honestly recorded | PASS | `implement/document-gaps.md`: Blocker No, security SEC-044-03 cited, spec text cited, owner (recovery tech lead / specification owner) and suggested `L-DYNAMIC-SQL`; RES-E044-01 withdrawn with the dynamic analysis; not silently accepted |
| Plan file list and shared files | PASS | Diff is exactly the plan's main, test, fixture, build, infra, README and `docs/stories/RWB-E1-044` files; only shared file `backend/build.gradle.kts` plus the two named infra init files; no `application*.yaml`, `scripts/dev.ps1`, frontend, API or CI change |
| D-RUN-17 base | PASS | Base and merge-base `f36991a` (RWB-TE-001 merged); `RecoveryFlywayConfig` is at `casewf.migration`; the TE-001 coverage wiring is inherited, not rebuilt |
| D-RUN-21 one module | PASS | Every main and test Java class is under `th.co.scb.ace.demo.recovery`; no other ACE module is read or created; `RecoveryBoundaryTest` and `ModulithTest` stay green |
| `AGENTS.md` section 9 sign-off | N/A | OPEN-016; no sign-off claimed in the report, plan, review or code; the implementation report ends `GATE_REVIEW: PENDING_ORCHESTRATOR` |
| Review evidence | PASS with CODE-003 | Security review PASS WITH FINDINGS (0 Critical / 0 High / 0 Medium / 4 Low / 1 Info); the four Lows are fixed in `c253b3c`, SEC-044-03 is the recorded gap; ponytail Must/Should/Nice fixes are in the code and tests, but its artifact is stale (CODE-003) |

## Notes

- The security review is "PASS WITH FINDINGS", not a bare PASS. That is consistent with its 4 Low and 1 Info findings; nothing there is Critical, High or Medium.
- The ponytail review's Must-fix items are closed by code and tests: `RecoveryMigrationRunner.failureObject` catches the detail lookup failure and keeps the original exception; `SequenceGapRule` reports `V0000`; the fail-closed folder, split-qualifier, type-aware drift, history-table constant, lexer bounds, header strip and dead-code findings are also fixed. Only the review file is stale (CODE-003).
- No production migration file is shipped and no merged migration is edited. No direct ACE `public` table is read by production code.
- The `implement/unit-tests/report.md` and `review/ponytail-review.md` staleness does not change any measured gate: the native reports and the final implementation report agree.

`REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.`

Pre-fix gate (superseded by the verification below): `CODE_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 3]`

## Code-gate fix verification (`89477bc`)

Verified against `89477bc` in `rwb-wt/RWB-E1-044`. The commit touches only
`LiteralSchemaRule.java` and the new `LiteralSchemaRuleTest.java` (`1cfe5f1..89477bc`).

- **CODE-001 closed.** `statementAt` now selects the enclosing statement by identifier-view offset
  range (`startOffset <= offset < endOffset`), and `check` passes `matcher.start(1)`. The new test
  parses a multi-line `CREATE TABLE` whose `REFERENCES public.t1(id)` is on line 3, asserts line 3, a
  non-null statement starting at line 2, `isAllowedQualifier(statement, "public")` false and
  `"pg_catalog"` true. With the old `startLine == line` lookup the result is null and the test fails.
  The full lint fixture list is unchanged: the current allow-list is statement-independent, so no
  lint result changed.
- **CODE-002 closed.** `implement/unit-tests/report.md` now records the final run: 243 passed,
  0 failed, 0 skipped, 27 classes, and the counters from
  `implement/code-gate-fix/recoveryCoverageReport.xml`: INSTRUCTION 7091/7523 = 0.9426,
  BRANCH 630/732 = 0.8607, LINE 1333/1406 = 0.9481, METHOD 339/346 = 0.9798, all at or above 0.80.
  The round-5, first-round and code-gate-fix snapshots are labelled.
- **CODE-003 closed.** `implement/deviations.md` DEV-E044-01 records 18 integration tests
  (12 `RecoveryMigrationIT` + 6 `RecoveryDatabaseIT`). `review/ponytail-review.md` ends with the
  closure and **Verdict: Ship**. `review/security-review.md` ends with
  `SECURITY_REVIEW: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0] [INFO: 2]`.
- **No new finding, no test weakening.** Only the offset lookup and one new test class were added;
  no existing test or fixture changed. Coverage stays above the 80% gate on all four counters; the
  small deltas from the prior run are the new lines and branches, and the new `*Test` class is
  excluded from the bundle by the existing filter. **D-RUN-14 evidence is unchanged:** the fix
  commit touches no `infra/` file, no migration and no main class; `20-grants.sql.inc` still grants
  only `USAGE ON SCHEMA public` and `ace_view_owner WITH INHERIT FALSE, SET TRUE`, with no table
  privilege, no CREATE and no ADMIN. T-044-17 and the 18-test container suite are unchanged.

Final verdict: **PASS** - 0 Critical / 0 High / 0 Medium / 0 Low.

CODE_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
