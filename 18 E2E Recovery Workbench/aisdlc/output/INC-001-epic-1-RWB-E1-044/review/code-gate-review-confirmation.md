# Code gate review (confirmation): RWB-E1-044

> Provenance: the Compliance Reviewer agent returned this review as text. The orchestrator saved it here.
> The wording is condensed slightly; the finding IDs, files, lines, required fixes and the gate line are unchanged.
> The orchestrator re-checked CONF-E044-01, -02, -03 and -06 against the code before triage.

| Field | Value |
|---|---|
| Run | `INC-001-epic-1-RWB-E1-044` |
| Reviewed | Merge `b1d7424` on `develop-recovery` (`b1d7424^1..b1d7424`) and the files at `27567ed` |
| Measured against | `specify/spec.md` v14-7 and `plan/plan.md` v2 |
| Reviewer | Compliance Reviewer, code gate mode, confirmation round (Claude Opus 5.5, high effort), read only |
| Why | The build, the pre-merge reviews and code gate rounds 1 and 2 ran in opencode on DeepSeek v4.1 Flash (D-RUN-26). This is an independent Opus 5.5 gate on what was merged |
| Not done | No tests or builds were run; post-merge `test`, `it` and `e2e` at `27567ed` are green per the build log |
| Out of scope | REVIEW-001 M10 (grants comment); evidence-audit H-04, H-06, H-07, M-03 |
| Rule | D-RUN-09: any finding, Low included, fails the gate |

## 1. Inputs read

- Main code: `MigrationPropertiesConfig`, `RecoveryMigrationProperties`, `RecoveryFlywayConfig`, `RecoveryMigrationRunner`.
- Lint tooling (test scope): `MigrationLexer`, `ParsedMigrationFile`, `MigrationLint`, `MigrationRules`, `MigrationFinding` and the 15 rule classes.
- Tests: `RecoveryMigrationLintTest` and its 55 fixture folders, `RecoveryMigrationRunnerTest`, `MigrationPropertiesConfigTest`, `RecoveryFlywayConfigTest`, `RecoveryMigrationIT` and its 10 Flyway fixture folders.
- Build and infra: `backend/build.gradle.kts`, `infra/postgres/init/20-grants.sql.inc`, `00-roles-and-databases.sh`, `db/modulemigration/recovery/README.md`.
- Evidence and records: `implement/`, `review/` (ponytail, security, code gate rounds 1 and 2), the run README, the merge commit, `AI-SDLC-BUILD-LOG.md`, AGENTS.md §3, §4, §8, §11.

## 2. Verdict

The runtime part conforms to the spec: the Flyway bean, the runner, the `rwb.schema` binding and the D-RUN-14
grants. Coverage and test-count figures match the files. The failures are in the migration lint and its
tests: the SPEC-007 item 1 and 2 checks have no test that would fail if they broke, one SPEC-007 item 2
position is not implemented, and L-GRANT's line view is weaker than the inherited rule.

## 3. Findings

| ID | Severity | Where | Finding | Required fix |
|---|---|---|---|---|
| CONF-E044-01 | Medium | `architecture/migration/rule/LiteralSchemaRule.java:55-57`; fixtures `t02-positions-fail`, `t02-types-fail`, `t02-quoted-fail`, `t06-format-fail`, AC5 | Every item-1 and item-2 fixture uses a known qualifier (`public`, `recovery`), which the item-4 collector already reports on the same deduplicated (rule, file, line, key). Removing the POSITION collector (line 56) leaves every test green. An unknown qualifier such as `rwb_case.t` or `"rwb_case".t`, the spec's own example, is never asserted (AC5, AC6, SPEC-007) | Fixtures with a non-known qualifier for every item-1 position and item-2 form (`CREATE TABLE rwb_case.t`, `"rwb_case".t`, `REFERENCES`, `FROM`/`JOIN`/`INTO`/`UPDATE`/`TRUNCATE`/`OWNED BY rwb_case.t`, `::rwb_case.ty`, `CAST(x AS rwb_case.ty)`), so that removing POSITION fails a test |
| CONF-E044-02 | Medium | `LiteralSchemaRule.java:39-43` | SPEC-007 item 2 lists a schema-qualified column data type in a column definition. POSITION has `::` and `AS` only, so `CREATE TABLE ${recoverySchema}.c1 (id rwb_case.t1);` passes. SPEC-007 says the list "may extend but not narrow"; no deviation records it | Detect a qualified column type in `CREATE TABLE`, `ALTER TABLE ... ADD COLUMN`, `ALTER COLUMN ... TYPE`, with failing and passing fixtures (or a recorded deviation with spec-gate approval) |
| CONF-E044-03 | Medium | `GrantRule.java:36, 53-56` | The line view accepts only `"GRANT "`/`"REVOKE "` (space). The inherited rule was `(?i)^\s*(grant\|revoke)\b`. A `GRANT<TAB>` line inside a `DO $$ … $$` or function body is missed by both views (the statement's first word is `DO`/`CREATE`). This weakens an inherited check (SPEC-009, AGENTS §4) | Word-boundary match on both views; fixtures with `GRANT<TAB>` and `REVOKE<TAB>` inside a DO body and a function body |
| CONF-E044-04 | Low | `casewf/migration/RecoveryMigrationRunner.java:69-71`; `RecoveryMigrationRunnerTest.java:103-108` | Any non-validate `FlywayException` reports `pending()[0]` when a pending version exists. The SPEC-003 table says a failure with no version (connection refused, lock timeout, missing schema) reports `recoveryFlyway`. The unit test stubs `pending()` empty, so cannot catch it | Limit the pending lookup to migration-execution failures (or record a deviation) and add a test with pending versions present |
| CONF-E044-05 | Low | `RecoveryMigrationProperties.java:20`; `MigrationPropertiesConfigTest.java` | No test binds `rwb.schema` absent or as `Recovery`, although plan T-044-08 claims null. Removing `@NotNull` or making the pattern case-insensitive stays green | Context-runner cases for absent and `Recovery`, asserting the bind exception and the D-RCV-28 message |
| CONF-E044-06 | Low | `MigrationLexer.java:24, 27, 34-44, 224-226` | `MAX_CHARACTERS = 262_144` and `MAX_DOLLAR_DEPTH = 32` (from SEC-044-05) narrow SPEC-010 (every file linted, no size limit) and are recorded only in the folder README. Physical Schema v6 is 925,733 bytes, so an RWB-E1-001 baseline built from it would be rejected | Record DEV-E044-05 and an open item or seam for RWB-E1-001 (split files, or a raised cap with a reason) |
| CONF-E044-07 | Low | `LiteralSchemaRule.java:39-43`; `db/modulemigration/recovery/README.md:56-57` | Bare `ON` and `AS` in POSITION report join aliases (`JOIN … b ON a.id = b.id` → "literal schema a"). SPEC-007 uses `ON` only in the object-name sense. README and IA-E044-06 document the `FROM`/`INTO` alias case only. Every RWB-E1-069 view join will hit this | Narrow `ON` to the spec's object-name forms with a passing `JOIN … ON a.id` fixture, or document the false positive and record an assumption |
| CONF-E044-08 | Low | `implement/code-map.md:32` | CODE-E044-028 says 50 lint fixture folders; `b1d7424` has 55 (matching 55 parameterised cases) | Dated correction note (merged evidence is history) |
| CONF-E044-09 | Low | run `README.md:21-27`; merge `b1d7424` line 5; `AI-SDLC-BUILD-LOG.md:413-420` | Merge and branch commits name Claude Code / Opus 5.5; the build, pre-merge reviews and original code gate ran in opencode on DeepSeek v4.1 Flash. The E1-042 and TE-002 READMEs disclose opencode; E1-044's does not (AGENTS §8) | Do not rewrite history. Add a Provenance section to the run README and a log correction row referencing this review |

## 4. Gate checklist

| Check | Result | Notes |
|---|---|---|
| Every AC has a test that would fail if the behaviour broke | FAIL | CONF-E044-01, -05. The runtime ACs (T-044-10..18, runner messages, D-RUN-14 rights) are discriminating |
| No test weakened or skipped | FAIL | CONF-E044-03. No `@Disabled` or skip. The `RecoveryFlywayConfigTest` change is the plan's allowed change (2) |
| AGENTS.md §3 | PASS | No production migration; `${recoverySchema}`; tooling is test scope |
| AGENTS.md §4 | FAIL (weakened check) | CONF-E044-03. No credentials (synthetic container values), no PII, `V0001` not edited |
| AGENTS.md §8 traceability | FAIL | CONF-E044-09 |
| Spec deviations recorded | FAIL | CONF-E044-02, -04, -06, -07 |
| Evidence figures match files | PARTIAL | Coverage at `code-gate-fix`: instruction 94.26%, branch 86.07%, line 94.81%, method 97.98%, matching XML, unit report and merge commit. 243 unit tests match the source count. Code map stale (CONF-E044-08) |
| D-RUN-14 grants | PASS | `USAGE ON SCHEMA public` and `ace_view_owner … WITH INHERIT FALSE, SET TRUE`; the IT asserts exactly these |
| No new dependency | PASS | Only `migrationToolingClasses` added to both JaCoCo tasks |
| Flyway configuration (SPEC-001/003/011-013) | PASS | `validateOnMigrate`, no out-of-order, clean disabled, baseline 0, own history table |
| DG-E044-DYN-01 (DG-013) | Recorded, Blocker No | Not re-raised |

## 5. Notes

- The original code gate (round 2 PASS at `89477bc`) raised none of CONF-E044-01..09.
- When fixed, add an AGENTS.md §11 entry for the CONF-E044-01 pattern: fixtures that a broader rule satisfies, so the narrower rule is never tested.
- Re-gate after the fixes (`dev.ps1 test`; `it` if the runner changes) and save the next round as `code-gate-review-confirmation-2.md`.

REVIEW_TYPE: CODE_GATE_REVIEW (CONFIRMATION)
CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 3] [LOW: 6]
