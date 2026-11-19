---
title: "RWB-E1-044 Database migrations versioned with parameterized schema names — documentation index"
run_id: "INC-001-epic-1-RWB-E1-044"
story: "RWB-E1-044"
epic: "EPIC-001"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED — code gate PASS; human review and merge not recorded"
branch: "feature/RWB-E1-044-db-migrations @ 89477bc (base f36991a, RWB-TE-001 merged)"
sources: "spec v14-7, plan v2, tasks v2, implementation report, unit-test report, code gate review, security review, ponytail review, implement/document-gaps.md"
---

# Recovery database migrations (RWB-E1-044)

**DOC ID:** DOC-RWB-E1-044-001 · **Maps to:** SPEC-RWB-E1-044-001..-017, AC1–AC9, TASK-00..TASK-19, CODE-E044-001..031

RWB-E1-044 is the build-order 1 story of EPIC-001 for the recovery module of ACE. Its subject is
"Database migrations versioned with parameterized schema names" (story files v7,
`rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md`). The story turns
the inherited Flyway bean and the inherited migration lint into the controls the Decision Log v10
row D-RCV-28 requires:

1. every change to schema `recovery` is a versioned, checksummed, forward-only Flyway migration;
2. the schema is named only as `${recoverySchema}` and is pinned to `recovery` in every environment;
3. every migration file is checked at build time by **15 lint rules** before merge;
4. a failed migration is reported once with `MSG-P3-016` and the version concerned, and the service
   does not start;
5. the schema produced by the migrations can be compared with a target, and each difference is
   reported as `MSG-P3-016 schema=recovery object=recovery.<table>.<column>`;
6. the migration account holds exactly the two narrow rights of orchestrator decision **D-RUN-14**
   for the ACE source views, and no ACE DBA role.

**This story ships no production migration file.** The production folder
`backend/src/main/resources/db/modulemigration/recovery/` holds `README.md` only. Every
`V<seq>__…sql` file in the branch is a test fixture under `backend/src/test/resources/`. That is
D-RCV-28 and story v7 §13, and the code gate verified it (D-RUN-07; zero `.sql` files in the
production folder).

## 1. What was built

| Deliverable | Where | SPEC |
|---|---|---|
| One-pass, quote-aware migration tokenizer and parsed file model (three line-preserving views) | `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/migration/` | SPEC-007, -016 |
| Lint registry with 15 rule IDs, one class per rule, one ordered registry | same package, `rule/` sub-package, `MigrationRules` | SPEC-004..-010, -016 |
| Lint fixtures: **55 folders**, every rule with failing and passing cases, plus the adversarial tokenizer corpus T-044-22 | `backend/src/test/resources/migration-lint/` | SPEC-010 |
| `rwb.schema=recovery` pin on the migration properties record, bound on every start | `casewf/migration/RecoveryMigrationProperties.java`, `MigrationPropertiesConfig.java` | SPEC-002 |
| `MSG-P3-016` failure report with the failing version(s) and a failed start | `casewf/migration/RecoveryMigrationRunner.java`, `RecoveryFlywayConfig.java` | SPEC-003 |
| Explicit `validateOnMigrate(true)` and the inherited Flyway settings kept | `casewf/migration/RecoveryFlywayConfig.java` | SPEC-001 |
| Schema snapshot reader and pure drift comparator | `architecture/migration/SchemaSnapshot*.java`, `SchemaComparator.java`, `SchemaDifference.java` | SPEC-012 |
| Container proof of Flyway behaviour (18 tests) | `casewf/migration/RecoveryMigrationIT.java`; `backend/src/test/resources/flyway-fixtures/` (10 folders) | SPEC-011..-013, -017 |
| D-RUN-14 migrator rights in the local init | `infra/postgres/init/20-grants.sql.inc`, `00-roles-and-databases.sh` | SPEC-017 |
| Coverage wiring: migration tooling joins the combined 80% bundle | `backend/build.gradle.kts` (JaCoCo class directories only) | SPEC-014 |
| Developer rule reference and story/plan convention | `backend/src/main/resources/db/modulemigration/recovery/README.md`; `docs/stories/RWB-E1-044/` | SPEC-015 |

No endpoint, controller, DTO, screen, route, feature flag, dependency or production migration is
added. Change classification: `ENHANCEMENT_LOGIC_ONLY`; UI In Scope `NO`; API In Scope `NO`;
`NO_API_CHANGE`. The frontend and `api/` are untouched.

## 2. The 15 lint rules

**DOC ID:** DOC-RWB-E1-044-002 · **Maps to:** SPEC-RWB-E1-044-004..-010, -016; AC5, AC6, AC7, BR8; TASK-03, TASK-04; CODE-E044-006, CODE-E044-008..019

Every finding is one line, in the Error and Message Standard v4 ID `MSG-P3-016`:

```text
MSG-P3-016 schema=recovery object=<file>:<line> rule=<RULE-ID> <detail>
```

`<line>` is 1-based; it is `0` for the file-level rules (name, sequence, header, key, fix). The test
fails listing **all** findings, not only the first. A finding's identity is
`(rule, file, line, key)`: one identity gives exactly one finding however many clauses or positions
matched; different identities give separate findings.

| Rule ID | Level | What it refuses | Basis |
|---|---|---|---|
| `L-NAME` | file | A name that does not match `^V(\d{4})__(rwb_[a-z0-9]+_\d{3})_[a-z0-9_]+\.sql$`; every non-`.sql` folder entry except `README.md` | D-RCV-28 (1); ASM-E044-05 |
| `L-UNDO` | file | Any `U*.sql` undo file | AC7; D-RCV-28 |
| `L-REPEATABLE` | file | Any `R__*.sql` repeatable file | D-RCV-28 |
| `L-SEQ-GAP` | file | A sequence that does not start at `0001` and stay contiguous; a `V0000` file | D-RCV-28 (1); ponytail Must 2 |
| `L-SEQ-DUP` | file | Two files with the same four-digit sequence; names both | D-RCV-28 (1) |
| `L-HEADER` | file | Line 1 other than `-- Story: <key derived from the file name>` (`rwb_e1_044` → `RWB-E1-044`) | D-RCV-28 |
| `L-HEADER-MULTI` | file | A second `-- Story:` line anywhere, including an indented one | D-RCV-28 |
| `L-KEY-DUP` | file | A second non-fix file for the same story key; names both files and the key | D-RCV-28 (1) |
| `L-FIX-LINE2` | file | A `-- Fix:` line 2 with an empty reason | D-RCV-28 |
| `L-FIX-NO-BASE` | file | A fix file without exactly one non-fix file of its key at a lower sequence | D-RCV-28 |
| `L-SEARCH-PATH` | line | The identifier `search_path` in any form: `SET`, `SET LOCAL`, `SET SESSION`, `RESET`, `ALTER ROLE/DATABASE/FUNCTION … SET`, and `set_config('search_path', …)` | D-RCV-28 (2); SPEC-007 |
| `L-LITERAL-SCHEMA` | line | A literal schema qualifier in an object-name position, a qualified type, a bare name after `SCHEMA`, or `recovery.` / `ace.` / `public.` anywhere in identifiers. Allowed: `${recoverySchema}`, `information_schema`, `pg_catalog` | D-RCV-28 (2); AC5; D-RUN-13 |
| `L-FK-OUTSIDE` | line | `REFERENCES <qualifier>.<table>` where the qualifier is not `${recoverySchema}` (BR8) | BR8; ADR-010; D-RCV-35 U4 |
| `L-GRANT` | line/statement | `GRANT` or `REVOKE` as the first word of a line or of a statement (`SELECT 1; GRANT …`) | BS-2.5, BS-2.6 |
| `L-LEX` | line | An unterminated string, escape string, quoted identifier, block comment or dollar-quoted body; one finding on the opener's line | SPEC-007; ASM-E044-16 |

Two properties make the rule set safe rather than cosmetic:

- **Identifiers only.** `L-LITERAL-SCHEMA` and `L-FK-OUTSIDE` ignore comments and string literals
  (D-RUN-13): a dictionary value such as `'public.account.account_key'` is data, not a schema
  reference. Dollar-quoted bodies are code and are scanned.
- **Fail closed.** A missing or unreadable folder or `.sql` entry raises an error; it never returns
  "no findings". A stray quote or comment opener cannot hide the rest of the file (the one-pass
  tokenizer and `L-LEX`).

The full rule table with examples is in
`backend/src/main/resources/db/modulemigration/recovery/README.md`.

## 3. Schema pin and failure mapping

**DOC ID:** DOC-RWB-E1-044-003 · **Maps to:** SPEC-RWB-E1-044-001, -002, -003, -013; AC3, AC4, AC7, AC8; NFR-027, NFR-052; TASK-08, TASK-10; CODE-E044-021..024

### Schema pinned to `recovery`

`rwb.schema` must bind to exactly `recovery`, whatever `rwb.flyway.enabled` is.

- `RecoveryMigrationProperties` is a package-private `@ConfigurationProperties(prefix = "rwb")`
  record whose first component is `schema`; the record carries `@Validated`, and `schema` carries
  `@NotNull` and `@Pattern(regexp = "recovery")`. Both messages read
  `rwb.schema must be recovery (D-RCV-28)`.
- `MigrationPropertiesConfig` is a package-private `@Configuration(proxyBeanMethods = false)` with
  `@EnableConfigurationProperties(RecoveryMigrationProperties.class)` and **no condition**. It
  registers the record on every start, so the check runs even when `RWB_FLYWAY_ENABLED=false`; it
  cannot be skipped with the Flyway bean.
- Validation happens when Spring binds the record, not in a compact constructor. Code that builds
  the record directly (as the inherited RWB-TE-001 tests do) is unaffected.
- A wrong, blank or null value is a start-up configuration error: Spring raises a
  `ConfigurationPropertiesBindException` whose root cause is a `BindValidationException`; the
  context fails and the service serves no request. This is a configuration error, not a user
  message, so no message ID applies (ASM-E044-03).
- `application.yaml` already binds `rwb.schema: recovery`; no key is added, renamed or defaulted, and
  the environment variable `RWB_SCHEMA` no longer changes it (audit A-17 closed).

**Deployment note.** An environment that sets `RWB_SCHEMA` to anything else now fails at start.
That is intended D-RCV-28 behaviour: remove the variable. `RWB_FLYWAY_ENABLED=false` does not avoid
it.

### Failure reported as `MSG-P3-016`

The Flyway factory method `recoveryFlyway(...)` builds and returns the bean and **never migrates**.
A separate `RecoveryMigrationRunner` bean is created with `initMethod = "migrate"`, so the migrate
runs only when the container initialises it. On a `FlywayException` the runner:

1. logs exactly **one** ERROR line `MSG-P3-016 schema={schema} object={object}` — the message ID and
   two parameters only, no SQL and no credential (BS-4.6, CLAR-004);
2. rethrows the original exception, so the context fails and the service does not start.

| Failure | `object` value | Source |
|---|---|---|
| Validation failure: checksum mismatch, applied file missing, or a lower pending version under `outOfOrder(false)` | The version or versions concerned, comma-separated, distinct, leading zeros removed (`0002` → `2`) | `Flyway.validateWithResult().invalidMigrations[].version` |
| Migration that fails part way | The version of the failed migration (the first pending version after the PostgreSQL rollback) | `Flyway.info().pending()` |
| No version available: connection refused, lock timeout, missing schema | `recoveryFlyway` | Fixed fallback |

The detail lookup is guarded: if `info()` or `validateWithResult()` fails too, the runner still
writes the fallback line and rethrows the original exception. A refused `clean()` is **not** wrapped;
it shows Flyway's own message (DG-L11).

### Forward only and rollback

- `cleanDisabled(true)` in every environment; no `U` file exists and `L-UNDO` refuses one.
- `outOfOrder(false)`; a lower pending version fails validation with its version.
- `ignoreMigrationPatterns` stays at Flyway's default (`*:future`), so a previous tag starts against
  a database that already holds a later version and applies nothing (NFR-027; T-044-13).
- Rollback is redeploying the previous tag. There is no undo path and no forward migration edit.

## 4. The drift check

**DOC ID:** DOC-RWB-E1-044-004 · **Maps to:** SPEC-RWB-E1-044-012; AC2, BR7; TASK-05, TASK-06, TASK-14; CODE-E044-020

Two test-scope parts, both under `architecture/migration/`:

- `SchemaSnapshotReader` reads one database's schema `recovery` from `information_schema` and
  `pg_catalog`: tables, columns (with the full type from `pg_catalog.format_type(atttypid, atttypmod)`
  and nullability), constraints, indexes and views with their column names. Only the JDBC call needs
  a database; `fromRows` is pure, so unit tests feed catalog rows in memory.
- `SchemaComparator` is pure logic. It compares two snapshots and formats each difference as
  `MSG-P3-016 schema=recovery object=recovery.<table>.<column>` (or the constraint, index or view
  name). Differences are added, missing or changed.

The container proof (T-044-15) applies the same fixtures to two clean databases, adds column
`note_x` to `recovery.queue` in one, and asserts exactly one difference naming
`recovery.queue.note_x`. Flyway's own history table `flyway_schema_history_recovery` is excluded
from the snapshot: its auto-generated constraint names embed OIDs and differ between identical
databases (DEV-E044-02).

**Not built, by decision.** There is no comparison against real SIT, UAT or PROD, no read-only drift
account and no `rwb.p3.migration-drift-gate` flag (D-RCV-05; D-RCV-44; OI-E044 parked). The
container-to-container check is the AC2 evidence here. A view column **type** change is not compared
(view columns are names only): a recorded follow-up, not a spec requirement.

## 5. How a developer runs it

**DOC ID:** DOC-RWB-E1-044-005 · **Maps to:** SPEC-RWB-E1-044-010, -011, -014; TASK-00..TASK-18

Set the JVM property in the shell; run the Gradle commands from `backend/` and the script from the
repository root (RUN-BRIEF "Local stack facts"):

```powershell
$env:JAVA_TOOL_OPTIONS="-Djdk.net.unixdomain.tmpdir=$env:USERPROFILE\.gradle\uds"
```

| Check | Command (from `backend/`) | Notes |
|---|---|---|
| All unit tests and the lint | `./gradlew test` | 243 tests in 27 classes. `RecoveryMigrationLintTest`, `MigrationLexerTest`, `SchemaComparatorTest`, `MigrationPropertiesConfigTest`, `RecoveryMigrationRunnerTest` and the inherited tests run here. `recoveryCoverageReport` runs as its finalizer. |
| Coverage gate (80% × 4) | `./gradlew test recoveryCoverageVerification` | `test` alone does **not** run the verification task, and `scripts/dev.ps1 test` does not either. |
| Lint only | `./gradlew test --tests "*RecoveryMigrationLintTest"` | Production folder plus all 55 fixture folders. |
| Tokenizer only | `./gradlew test --tests "*MigrationLexerTest"` | Adversarial cases T-044-22 and statement view S1. |
| Drift comparator only | `./gradlew test --tests "*SchemaComparatorTest"` | Pure comparison and catalog-row mapping. |
| Container suite | `./gradlew recoveryIntegrationTest` | 18 tests: 12 `RecoveryMigrationIT` + 6 `RecoveryDatabaseIT`. Docker required; the task fails, not skips, without it. |
| Repository merge gate | `./scripts/dev.ps1 test` (repo root) | Runs `gradlew test` and `npm run check`. In this session the wrapper could not run because of a workstation issue (DEV-E044-01); its two halves were run directly and both exited 0. |

### Adding a recovery migration

This story ships none, but the procedure the lint enforces is:

1. Put the file in `backend/src/main/resources/db/modulemigration/recovery/`.
2. Name it `V<seq>__rwb_e1_044_<name>.sql`. `<seq>` is the next free four-digit number **in merge
   order**; never fix it in advance (D-RCV-28, D-RUN-07). The sequence must be contiguous from
   `V0001`.
3. Line 1 is `-- Story: RWB-E1-044`.
4. Refer to the schema only as `${recoverySchema}`. No `recovery.`, `ace.` or `public.` qualifier; no
   `SET search_path`; no `GRANT`/`REVOKE`; no foreign key out of the schema.
5. A corrective file takes the next sequence, keeps the story key and adds line 2
   `-- Fix: <reason>`.
6. Run `./gradlew test --tests "*RecoveryMigrationLintTest"` before committing; the complete finding
   list must be empty.
7. Never edit a merged migration. `clean` stays disabled.

Every `V<seq>` name in this story's fixtures uses a concrete number only because the lint checks
contiguity from `V0001`; fixtures are test data, not migrations.

## 6. Status and gates

**DOC ID:** DOC-RWB-E1-044-006 · **Maps to:** SPEC-RWB-E1-044-014; TASK-13, TASK-17, TASK-18, TASK-19

| Gate or check | Result | Evidence |
|---|---|---|
| Spec gate | **PASS** round 7, 0 Critical / 0 High / 0 Medium / 0 Low; 28/28 requirement rows | `../review/spec-gate-review-7.md`; spec v14-7 |
| Plan gate | **PASS** round 2, 0/0/0/0; 20 tasks; every SPEC-001..-017 mapped | `../review/plan-gate-review-2.md`; plan v2 |
| Code gate | **PASS** 0 Critical / 0 High / 0 Medium / 0 Low at `89477bc`; CODE-001..003 closed and verified | `../review/code-gate-review.md` |
| Backend unit | 243 passed, 0 failed, 0 skipped (27 classes) | `../implement/unit-tests/report.md`; `../implement/code-gate-fix/unit-coverage.log` |
| Backend coverage | LINE 94.81%, INSTRUCTION 94.26%, BRANCH 86.07%, METHOD 97.98% — each ≥ 80%; `recoveryCoverageVerification` exit 0 | `../implement/code-gate-fix/recoveryCoverageReport.xml` |
| Container | 18 passed (12 `RecoveryMigrationIT` + 6 `RecoveryDatabaseIT`), 0 failed, 0 skipped, exit 0 | `../implement/review-fix/it.log` |
| Frontend regression | 28 Vitest tests passed; typecheck, lint and coverage exit 0. Unchanged by this story | `../implement/merge-gate.log` |
| Security review | **PASS** after fixes: 0 Critical / 0 High / 0 Medium / 0 Low / 2 Informational | `../review/security-review.md` |
| Ponytail review | **Ship**; all Must/Should/Nice items closed except the view-column-type follow-up (Nice 9) | `../review/ponytail-review.md` |
| Functional automation | `NOT_APPLICABLE`: no UI, screen or route; the same checks run as unit tests | plan v2 "Functional Test Scenarios" |
| API tests | `NOT_APPLICABLE`: `NO_API_CHANGE`; no endpoint added or changed | spec v14-7 "API Change Assessment" |
| Human review / merge | **Not recorded.** No approver name, `AGENTS.md` §9 sign-off, merge, release, SIT or UAT result is claimed | code gate notes; OPEN-016 |

**Documentation snapshot.** The branch is `feature/RWB-E1-044-db-migrations`, tip `89477bc`, base
`f36991a` (RWB-TE-001 merged by D-RUN-17). The documentation describes that tip. No production
migration, endpoint, dependency or frontend file is part of the delta.

## 7. Documents in this folder

| Document | Purpose |
|---|---|
| `README.md` (this file) | What the migration tooling is, the 15 rules, the schema pin and failure mapping, the drift check, how to run it, status and gates. |
| `ARCHITECTURE.md` | Tokenizer and views, lint registry and extension point, snapshot and comparator, Flyway configuration, D-RUN-14 grants, the no-production-migration boundary and coverage wiring. |
| `COMPLIANCE.md` | AC/SPEC/TASK/test trace, 80% evidence, reviews and the dynamic-SQL gap, deviations, open items with no approval claimed. |
| `assumptions.md` | Documentation-stage assumptions (`A-DOC-E044-*`). |
| `shared-updates.md` | Rows this stage would add to the shared registers; the stage writes none of them. |
| `document-gaps.md` | Documentation-stage gap check (no new gap; DG-E044-DYN-01 carried). |

### DOC ID index

| DOC ID | Where | Maps to |
|---|---|---|
| DOC-RWB-E1-044-001 | README §1 | SPEC-001..-017; AC1–AC9; TASK-00..-19; CODE-E044-001..031 |
| DOC-RWB-E1-044-002 | README §2 | SPEC-004..-010, -016; AC5, AC6, AC7; BR8; TASK-03, -04; CODE-E044-006, -008..-019 |
| DOC-RWB-E1-044-003 | README §3 | SPEC-001, -002, -003, -013; AC3, AC4, AC7, AC8; NFR-027, NFR-052; TASK-08, -10; CODE-E044-021..024 |
| DOC-RWB-E1-044-004 | README §4 | SPEC-012; AC2; BR7; TASK-05, -06, -14; CODE-E044-020 |
| DOC-RWB-E1-044-005 | README §5 | SPEC-010, -011, -014; TASK-00..-18 |
| DOC-RWB-E1-044-006 | README §6 | SPEC-014; TASK-13, -17, -18, -19 |
| DOC-RWB-E1-044-007 | ARCHITECTURE §2 | SPEC-007, -016; AC5; D-RUN-13; TASK-01, -02; CODE-E044-001..004 |
| DOC-RWB-E1-044-008 | ARCHITECTURE §3 | SPEC-004..-010, -016; TASK-03, -04; CODE-E044-005..019 |
| DOC-RWB-E1-044-009 | ARCHITECTURE §4 | SPEC-012; AC2; TASK-05, -06, -14; CODE-E044-020 |
| DOC-RWB-E1-044-010 | ARCHITECTURE §5 | SPEC-001, -002, -003, -013; AC1, AC3, AC4, AC7, AC8; NFR-027, NFR-052; TASK-08, -10, -14; CODE-E044-021..024 |
| DOC-RWB-E1-044-011 | ARCHITECTURE §6 | SPEC-017; BR8; D-RUN-14; TASK-11, -12; CODE-E044-026 |
| DOC-RWB-E1-044-012 | ARCHITECTURE §7 | SPEC-014, -015; D-RUN-07; TASK-13, -16; CODE-E044-025, -030, -031 |
| DOC-RWB-E1-044-013 | COMPLIANCE §2 | AC1–AC9; T-044-01..-22; TASK-03..-14 |
| DOC-RWB-E1-044-014 | COMPLIANCE §3 | BR1–BR8; D-RCV-28, D-RUN-13, D-RCV-48; NFR-027, NFR-052; TASK-03..-19 |
| DOC-RWB-E1-044-015 | COMPLIANCE §4 | SPEC-014; TASK-13, TASK-17 |
| DOC-RWB-E1-044-016 | COMPLIANCE §5 | SPEC-003, -009; TASK-18, TASK-19; DG-E044-DYN-01 |
| DOC-RWB-E1-044-017 | COMPLIANCE §6 | TASK-00, -03, -09, -10, -15, -18; DEV-E044-01..04; IA-E044-01..07 |
| DOC-RWB-E1-044-018 | COMPLIANCE §7 | SPEC-017; OI-E044-A..J; OPEN-016, OPEN-050 |

No `OPERATIONS.md` is published. The story adds no job, queue, monitor, endpoint or flag to operate;
the only repeatable procedures are the developer and merge-gate commands in §5, and the operational
effect of a bad migration is one `MSG-P3-016` ERROR line and a failed start (§3).

## 8. Changing a rule

The lint is a build-time control, and a rule change is a normal merge request with a gated spec
change, a failing fixture first and a passing fixture after. Adding a rule is one new
`MigrationRule` class plus one entry in `MigrationRules.all()`; no other rule changes (SPEC-016).
Never widen `isAllowedQualifier` or delete a fixture to turn a red build green. The one planned
extension is RWB-E1-069's narrow `public` exception for `CREATE [OR REPLACE] VIEW
${recoverySchema}.v_ace_*` (SEAM-E044-01), which comes with that story's own fixtures.
