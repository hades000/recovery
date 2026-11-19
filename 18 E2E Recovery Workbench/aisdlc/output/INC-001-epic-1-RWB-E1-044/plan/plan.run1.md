---
title: "Implementation Plan: RWB-E1-044 Database migrations versioned with parameterized schema names"
run_id: "INC-001-epic-1-RWB-E1-044"
story: "RWB-E1-044"
epic: "EPIC-001"
status: "SUCCESS"
revision: "v1 (18 Nov 2026): first plan stage for this run. Written against spec v14-7 (spec gate round 7, PASS 0/0/0/0) and the RWB-TE-001 plan v7 package layout, coverage wiring and test names (orchestrator decision D-RUN-17)."
prepared: "2026-11-18"
---

# Implementation Plan: RWB-E1-044 Database migrations versioned with parameterized schema names

Design Source: `NOT_REQUIRED` (UI In Scope: NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` in `../specify/spec.md`).

| Field | Value |
|---|---|
| Spec | `../specify/spec.md` v14-7. Spec gate round 7: `PASS` 0 Critical / 0 High / 0 Medium / 0 Low (`../review/spec-gate-review-7.md`). `Status: SUCCESS`; `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 28] [MISSING_RULES: 0] [CONTRADICTIONS: 0]`. |
| Story | Story files v7, `rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md` (read through §1–§16). |
| Base layout (D-RUN-17) | RWB-TE-001 plan v7 (`../../INC-002-epic-1-RWB-TE-001/plan/plan.md`, `tasks.md`, `data-model.md`) and its plan gate round 7 (`PASS` 0/0/0/0). RWB-TE-001 merges before this story. |
| Code base | This repository as read on 18 Nov 2026: `backend/src/main/java/th/co/scb/ace/demo/recovery/**` (today's pre-TE-001 layout), `backend/src/test/java/th/co/scb/ace/demo/**`, `backend/build.gradle.kts`, `backend/src/main/resources/application.yaml`, `infra/postgres/init/**`, `infra/postgres/schema/01-ace-schema-v1.sql`. Flyway 12.4.0 read with `javap` from the local Gradle cache. No git command, container or build was run; no file outside `plan/` was written. |
| Paths | Every path is the file's path as it is in this repository on `develop-recovery` today, **except** the RWB-TE-001 v7 paths, which exist only after TE-001 merges (marked `[TE-001]` below). |
| Builder | Implementation Builder in its own git worktree from `develop-recovery` **after** the RWB-TE-001 merge. Commits `RWB-E1-044: <summary>` with the `AISDLC-Run` and `AISDLC-Plan` trailers. |
| Smallest change | Extend the inherited Flyway bean and replace the inherited lint test logic with a test-scope tooling package; add one unconditional registration class, one failure-reporting runner, test-scope comparator and fixtures, one local-init grant block, one build-file edit and one README edit. No new dependency, endpoint, screen, production migration, pipeline or frontend change. |

## Upstream readiness

| Check | Result |
|---|---|
| Spec status | `SUCCESS` (spec front matter; Status section) |
| Spec gate | `PASS` round 7, 0 findings (`../review/spec-gate-review-7.md` §9) |
| `REQUIREMENT_COVERAGE_RESULT` | `MISSING_RULES: 0`, `CONTRADICTIONS: 0` (28 rules; 8 source contradictions settled) |
| Clarification log | CLAR-001 to CLAR-013 all `RESOLVED`. No `OPEN` row. |
| Design evidence | `NOT_REQUIRED` (UI In Scope NO): no screen task, no `frontend/` file, no `frontend/components.md`. |
| Production migration | None. D-RUN-07 is not exercised (`## Migrations` below). |
| Base dependency | RWB-TE-001 plan v7 is gated (`PASS` 0/0/0/0) and merges first (D-RUN-17). This plan names its paths and its registration case. |

`PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]`. The 9 spec open items (OI-E044-A, -B, -C, -D, -E, -F, -G, -I, -J) are shared open-item candidates that other owners answer; none is a `CLAR-*` item and none blocks this plan. OI-E044-H and OI-E044-K are closed.

## RWB-TE-001 v7 base (D-RUN-17) — the three cases this plan settles

The spec leaves three details to RWB-TE-001's gated plan (`../specify/spec.md` SPEC-002, SPEC-014, SPEC-016, ASM-E044-19). They are settled here from plan v7 and are re-checked by the builder at TASK-00.

| Case | What RWB-TE-001 plan v7 says | Case that applies to E1-044 | Where applied |
|---|---|---|---|
| Package and class of the Flyway bean and of the migration properties record | `RecoveryFlywayConfig` moves to `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/migration/RecoveryFlywayConfig.java` (P3, package-private; plan.md Relocation row). `RecoveryProperties` is deleted and replaced by four package-private records. The P3 record is `RecoveryMigrationProperties(String schema, Flyway flyway)` at `.../casewf/migration/RecoveryMigrationProperties.java`, prefix `rwb`, nested `Flyway(boolean enabled, String url, String user, String password, String location)` (plan.md "Property split" row). | Names taken as they are. No E1-044 name is invented for them. | TASK-00, TASK-08, TASK-09, TASK-10, TASK-14 |
| Registration of `RecoveryMigrationProperties` | Registered by `@EnableConfigurationProperties` **on `RecoveryFlywayConfig`** (plan.md "Property split", column "Registered by"). That class carries `@ConditionalOnProperty(name = "rwb.flyway.enabled", …)` today, so the registration is conditional. | **Case 1 of SPEC-002:** E1-044 moves the registration to a new unconditional package-private class, `MigrationPropertiesConfig`, in the same package. If the merged code instead registers it from an unconditional class already, TASK-08 adds nothing and TASK-00 records that. | TASK-07, TASK-08 |
| Tooling class directory in the coverage tasks | Plan.md "Coverage gate edit" and TASK-01: `boundaryToolingClasses` includes only `th/co/scb/ace/demo/recovery/architecture/boundary/**`, excluding `*Test` classes. That include does **not** take in `architecture/migration/**`. | **Case 1 of SPEC-014:** E1-044 adds its own tooling directory to `classDirectories` of both JaCoCo tasks (one edit, no new task or rule). | TASK-13 |

Also taken from plan v7: the binding-test helper `backend/src/test/java/th/co/scb/ace/demo/testsupport/ApplicationYamlEnvironment.java` (test scope), and the affected RWB-TE-001 test `backend/src/test/java/th/co/scb/ace/demo/recovery/casewf/migration/RecoveryFlywayConfigTest.java` (method `bindsSchemaAndFlywayFromApplicationYaml`, T-TE001-12). SPEC-002 "Existing tests" allows at most two changes to that test, with no assertion changed; this plan needs **change (2) only** — adding `MigrationPropertiesConfig` to the test's user configuration — because `application.yaml` line 74 already binds the literal `recovery` (`rwb.schema: recovery`), so no input changes. Change (1) does not apply. TASK-00 confirms the exact test setup in the merged code; a test that would need any other change is a stop-and-report (PG-E044-03).

## Change scope and surfaces

| Field | Value | Evidence |
|---|---|---|
| Change type | `ENHANCEMENT_LOGIC_ONLY` | Spec Change Scope Declaration; inherited Flyway bean and lint (audit A-04) |
| Backend | **CHANGED** — unit tests `REQUIRED` | `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/migration/**`, test-scope tooling, `backend/build.gradle.kts`, `infra/postgres/init/**` |
| Frontend | **NOT_APPLICABLE** — no unit test task | UI In Scope NO; story v7 §15 "No new screen in this story"; no file under `frontend/` changes; `frontend-integrations.json` records the N/A |
| API | `NO_API_CHANGE` — no API task | No endpoint, controller, route or DTO changes; `GET /api/recovery/v1/admin/jobs` and its migration-run part stay out of scope (D-RCV-12; SPEC-017) |
| UI | NO | `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`; `SCR-44` out of scope |
| Migration | **NONE** | Decision Log v10 D-RCV-28 and story v7 §13 ("ships no production migration file"); see `## Migrations` |
| Shared files edited | `backend/build.gradle.kts` (JaCoCo class directory only, D-RCV-40) | TASK-13 |
| New dependency | None | `spring-boot-starter-validation` is already `implementation` (`backend/build.gradle.kts` line 44); logback-classic is already on the test runtime through Spring Boot logging; Testcontainers PostgreSQL is already `testImplementation` (line 80) |

## Scope

In scope. Each bullet maps to tasks in `tasks.md` (see its "Scope bullet to task map"):

1. **S-1 Lint structure and tokenizer** — one quote-aware tokenizer pass, the three views, statements cut at top-level `;`, `L-LEX` (SPEC-007, -016). → TASK-01, -02, -03, -04
2. **S-2 Rule set and finding format** — the 15 rule IDs, `MSG-P3-016 schema=recovery object=<file>:<line> rule=<RULE-ID> <detail>`, finding multiplicity (SPEC-004, -005, -006, -007, -008, -009). → TASK-03, -04
3. **S-3 Lint testability and fixtures** — folder in, findings out; one failing and one passing fixture per rule; production folder green on README only (SPEC-010). → TASK-03, -04
4. **S-4 Schema pinned to `recovery`** — `@Validated` on the migration properties record, `@NotNull` + `@Pattern(regexp = "recovery")`, unconditional registration (SPEC-002). → TASK-07, -08
5. **S-5 Failure reported as MSG-P3-016** — one ERROR line with the schema and the version(s), rethrow, no migrate in the factory (SPEC-003). → TASK-09, -10
6. **S-6 Recovery Flyway bean settings** — extend, do not duplicate; explicit `validateOnMigrate(true)`; every inherited setting kept (SPEC-001). → TASK-08, -10
7. **S-7 Container proof of Flyway behaviour** — one container test class for apply-once, two databases, changed file, clean refusal, previous tag, part-way failure, concurrency, baseline (SPEC-011). → TASK-11, -12, -14, -15
8. **S-8 Drift comparison** — `SchemaSnapshotReader` + pure `SchemaComparator`, unit and container proof (SPEC-012). → TASK-05, -06, -14
9. **S-9 Forward only and rollback by previous tag** — `*:future` default, `outOfOrder(false)`, lower pending version fails with its version (SPEC-013). → TASK-10, -14
10. **S-10 Migrator rights for the ACE views (D-RUN-14)** — R1 `USAGE ON SCHEMA public` with no table privilege, R2 `ace_view_owner` membership `INHERIT FALSE, SET TRUE`, local init only, role comments reworded (SPEC-017). → TASK-11, -12
11. **S-11 Coverage gate** — this story's tooling added to RWB-TE-001's combined 80% bundle; baseline at the builder's first step (SPEC-014). → TASK-13, -17
12. **S-12 Documentation and convention** — migration-folder README, `docs/stories/RWB-E1-044/story.md` and `plan.md` (SPEC-015). → TASK-16
13. **S-13 Seams and exclusions** — SEAM-E044-01/-02/-03/-04 named and not built (SPEC-016, -017). → TASK-19 (checked), named in TASK-04 and TASK-16

Out of scope (SPEC-016, SPEC-017; each a named seam or a recorded exclusion): the `public` qualifier exception for RWB-E1-069 views (SEAM-E044-01), the Section A grants and two-non-fix-files resolution (SEAM-E044-02), job-monitor parts with no named owner (SEAM-E044-03, D-RCV-12, OI-E044-G), real-environment drift with a read-only account and `rwb.p3.migration-drift-gate` (D-RCV-05), the ACE DBA role for the migration account (declined, DG-L13), ACE-only `db-migrate`/H2/Jenkins items (ASM-E044-09), and any RWB-TE-001 work (SEAM-E044-04, already merged).

## One-module check (D-RUN-21)

`AGENTS.md` §7 and §9 ask that a plan "touches one module". Build decision D-RUN-21 (`AI-SDLC-BUILD-LOG.md` decisions table, 18 Nov 2026 05:36, the orchestrator (Claude Code); ratification tracked as OPEN-050, owner the recovery tech lead) settles the reading: **"touches one module" means the ACE module, the recovery module.**

| Check | Result |
|---|---|
| ACE module touched | `recovery` only — every main and test class is under `th.co.scb.ace.demo.recovery` |
| Nested design modules touched | P3 `casewf.migration` only (main); test scope `recovery.architecture.migration` (outside the module map, which reads main classes only, RWB-TE-001 SPEC-004/-011) |
| Other ACE modules | None. No `common`, `collection`, `platform`, `rules`, `workflow`, `documents` package is created or read; the packages RWB-TE-001 deletes are not referenced |
| Non-Java files touched | `backend/build.gradle.kts` (shared build file, D-RCV-40), `infra/postgres/init/**` (infrastructure init, not an ACE application module), `backend/src/main/resources/db/modulemigration/recovery/README.md`, `docs/stories/RWB-E1-044/**` |
| Verdict | **PASS — one module (recovery).** No return to the analyst is required on the one-module rule. |

Module boundary evidence: `RecoveryBoundaryTest` and `ModulithTest` stay green (TASK-17) and no new main class leaves `casewf.migration`.

## OI-E044-K coverage handling (D-RUN-17)

OI-E044-K (the 17 Nov 2026 recovery main-scope shortfall: LINE 133/415, BRANCH 25/92, INSTRUCTION 686/2174, METHOD 41/135) was closed by orchestrator decision D-RUN-17. This plan applies the closure as follows; it does not re-open it, and it claims no human ruling.

| Item | How this plan handles it |
|---|---|
| Gate | `recoveryCoverageVerification` stays one `BUNDLE` rule with LINE, INSTRUCTION, BRANCH and METHOD at `0.80` (RWB-TE-001 SPEC-020 (a)); no waiver, no exclusion, no lowered threshold, no narrowed class set. |
| Measured set | RWB-TE-001's combined bundle: all main classes under `th/co/scb/ace/demo/recovery/**` **plus** its boundary tooling **plus** this story's `architecture/migration/**` tooling (SPEC-014; TASK-13). |
| Baseline | TASK-00 runs `./gradlew test recoveryCoverageReport` on the merged RWB-TE-001 code **before any E1-044 change** and saves the four counters. The plan requires no baseline figure; it requires the report file and the counters in `implement/backend/coverage/baseline-recoveryCoverageReport.xml` + `baseline-counters.txt`. |
| What this story tests | Only the classes it changes or adds: `RecoveryMigrationProperties`, `MigrationPropertiesConfig`, `RecoveryFlywayConfig`, `RecoveryMigrationRunner` (T-044-08, T-044-09) and its tooling (T-044-01..-07, -19..-22). It writes **no** test for a class it does not change (SPEC-014 "Baseline and sequencing"). |
| If the bundle is below 80% at the code gate | The implementation reports a **blocker**. It never excludes a class, lowers a threshold, narrows the class set or shows the gate as passing (SPEC-014; `implementation-execution-gates.md`). |
| Integration coverage | Container coverage does not substitute for unit coverage (S-GATES). That is why SPEC-012 splits the comparator into a pure part reached by T-044-19. |

## Frontend Plan

**NOT_APPLICABLE.** UI In Scope NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`; story v7 section 15 says "No new screen in this story". No file under `frontend/` is added or changed, no frontend unit-test or coverage task is created, and `frontend/components.md` is not required (no affected component, screen or flow). The unchanged frontend is still verified by `npm run check` in the merge gate (TASK-18). `contracts/frontend-integrations.json` records the N/A with this evidence.

## Backend Plan

Surface status: **CHANGED**. Unit tests **REQUIRED** (trace SPEC-001..-017; gate as above).

### Files added or changed — main

`R` = `backend/src/main/java/th/co/scb/ace/demo/recovery`. `[TE-001]` marks a path that exists only after RWB-TE-001 merges.

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Edit `[TE-001]` | `R/casewf/migration/RecoveryFlywayConfig.java` — remove `@EnableConfigurationProperties`; add `validateOnMigrate(true)`; drop `initMethod = "migrate"` from `recoveryFlyway`; add the `recoveryMigrationRunner` bean | TASK-08, TASK-10 | 001, 002, 003 |
| Edit `[TE-001]` | `R/casewf/migration/RecoveryMigrationProperties.java` — `@Validated` on the record; `@NotNull @Pattern(regexp = "recovery", message = "rwb.schema must be recovery (D-RCV-28)")` on `schema`; keys, defaults and components unchanged | TASK-08 | 002 |
| Add | `R/casewf/migration/MigrationPropertiesConfig.java` — package-private `@Configuration(proxyBeanMethods = false)` + `@EnableConfigurationProperties(RecoveryMigrationProperties.class)`, no condition | TASK-08 | 002 |
| Add | `R/casewf/migration/RecoveryMigrationRunner.java` — package-private; one `migrate()` that wraps `flyway.migrate()`; one ERROR line; rethrow; `static String failureObject(Flyway, FlywayException)` | TASK-10 | 003 |

Not changed: `AceRecoveryApplication`, every other main class (RWB-TE-001's relocation and property split are inherited and stay as merged), `application.yaml` (line 74 already binds `rwb.schema: recovery`; no key is added or renamed), `application-local.yaml`, `backend/src/main/resources/db/modulemigration/recovery/*.sql` (none exists), `.gitlab-ci.yml`, `scripts/dev.ps1`, `frontend/**`, `api/**`.

### Files added or changed — test scope and fixtures

`T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`. All tooling is in the test source set, so the main module map and `ModulithTest` never see it.

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Add | `T/architecture/migration/MigrationLexer.java` — the one quote-aware pass and the token list | TASK-02 | 007 |
| Add | `T/architecture/migration/ParsedMigrationFile.java` — name, raw lines, code text (a), identifier text (b), statements (c), unterminated openers | TASK-02 | 007 |
| Add | `T/architecture/migration/MigrationStatement.java` — offset range, start line, first word, kind | TASK-02 | 007 |
| Add | `T/architecture/migration/LexProblem.java` — token kind and opener line for `L-LEX` | TASK-02 | 004, 007 |
| Add | `T/architecture/migration/MigrationFinding.java` — rule, file, line, key, detail; `format()` gives the SPEC-004 line | TASK-02 | 004 |
| Add | `T/architecture/migration/MigrationRule.java` — `ruleId()`, `check(ParsedMigrationFile, FolderContext)` | TASK-02 | 016 |
| Add | `T/architecture/migration/FolderContext.java` — the folder's parsed files, for file-level rules | TASK-02 | 005, 006 |
| Add | `T/architecture/migration/MigrationLint.java` — `static List<MigrationFinding> lint(Path folder)`; scans `*.sql`, keeps one tokenizer pass per file, runs the registry, returns all findings | TASK-04 | 004, 010 |
| Add | `T/architecture/migration/MigrationRules.java` — the one ordered registry (15 rules) | TASK-04 | 016 |
| Add | `T/architecture/migration/rule/*.java` — 15 rule classes, one per rule ID: `NameRule`, `UndoRule`, `RepeatableRule`, `SequenceGapRule`, `SequenceDuplicateRule`, `HeaderRule`, `HeaderMultiRule`, `KeyDuplicateRule`, `FixLine2Rule`, `FixNoBaseRule`, `SearchPathRule`, `LiteralSchemaRule`, `ForeignKeyOutsideRule`, `GrantRule`, `LexRule` | TASK-04 | 004..009, 016 |
| Edit | `T/architecture/RecoveryMigrationLintTest.java` — becomes the JUnit entry point: production folder + every fixture folder; asserts `rule`, `file`, `line` and, where two findings share a line, the key; asserts the full finding list | TASK-03 | 004, 010 |
| Add | `T/architecture/migration/MigrationLexerTest.java` — token kinds, nesting, escapes, unterminated openers, statement cut, statement-view case S1 | TASK-01 | 007 |
| Add | `T/architecture/migration/SchemaSnapshot.java` — tables, columns (type, nullability), constraints, indexes, views | TASK-06 | 012 |
| Add | `T/architecture/migration/SchemaSnapshotReader.java` — catalog rows to `SchemaSnapshot`; the row mapping is pure, only the JDBC read needs a database | TASK-06 | 012 |
| Add | `T/architecture/migration/SchemaComparator.java` — pure comparison and `MSG-P3-016 schema=recovery object=recovery.<…>` formatting | TASK-06 | 012 |
| Add | `T/architecture/migration/SchemaDifference.java` — kind (added/missing/changed), object path | TASK-06 | 012 |
| Add | `T/architecture/migration/SchemaComparatorTest.java` — T-044-19 | TASK-05 | 012 |
| Edit `[TE-001]` | `T/casewf/migration/RecoveryFlywayConfigTest.java` — **one** change only: add `MigrationPropertiesConfig` to the user configuration of `bindsSchemaAndFlywayFromApplicationYaml` (allowed change (2)); no assertion changed | TASK-08 | 002 |
| Add | `T/casewf/migration/MigrationPropertiesConfigTest.java` — T-044-08 cases (1)–(6) | TASK-07 | 002 |
| Add | `T/casewf/migration/RecoveryMigrationRunnerTest.java` — T-044-09 with a mocked `Flyway` | TASK-09 | 003, 001 |
| Add | `T/casewf/migration/RecoveryMigrationIT.java` — the **one** container test class, `@Tag("recovery-it")`, T-044-17 and T-044-10..T-044-18 | TASK-11, TASK-14 | 011, 012, 013, 017 |
| Add | `backend/src/test/resources/migration-lint/**` — the lint fixture corpus (`data-model.md` §3) | TASK-03 | 010 |
| Add | `backend/src/test/resources/flyway-fixtures/**` — the Flyway fixture corpus (`data-model.md` §4) | TASK-14 | 011 |
| Unchanged | `[TE-001]` `T/architecture/RecoveryBoundaryTest.java`, `th/co/scb/ace/demo/ModulithTest.java`, `T/RecoveryDatabaseIT.java`, `th/co/scb/ace/demo/e2e/PlatformE2ETest.java`, `T/testsupport/ApplicationYamlEnvironment.java` | — | 001, 014 |

### Files added or changed — build, infra and docs

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Edit | `backend/build.gradle.kts` — add a `migrationToolingClasses` file collection (test output, include `th/co/scb/ace/demo/recovery/architecture/migration/**`, exclude `**/*Test.class`, `**/*Test$*.class`, `**/*IT.class`, `**/*IT$*.class`); `classDirectories.setFrom(recoveryClasses, boundaryToolingClasses, migrationToolingClasses)` on **both** JaCoCo tasks; add test `java.srcDirs` to `sourceDirectories` of both if RWB-TE-001's edit does not already cover it. No new task, rule, counter, threshold or exclusion; execution data `test`; tasks stay outside `check` | TASK-13 | 014 |
| Edit | `infra/postgres/init/20-grants.sql.inc` — after `REVOKE ALL ON SCHEMA public FROM PUBLIC;`: `GRANT USAGE ON SCHEMA public TO rwb_migrator;` and `GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE;`; reword the line-9 comment | TASK-12 | 017 |
| Edit | `infra/postgres/init/00-roles-and-databases.sh` — comment text only, the `rwb_migrator` and `ace_view_owner` lines of the role list | TASK-12 | 017 |
| Edit | `backend/src/main/resources/db/modulemigration/recovery/README.md` — rule IDs, finding format and multiplicity, the `FROM`/`INTO` lexical note, the RWB-E1-069 seam, the `V0001`-to-`V0003` sentence reworded with no number fixed | TASK-16 | 015 |
| Add | `docs/stories/RWB-E1-044/story.md` — story key, links to the story v7 path and the spec, restated ACs | TASK-16 | 015 |
| Add | `docs/stories/RWB-E1-044/plan.md` — this plan, committed with the code (PG-E044-01) | TASK-16 | 015 |

### Tooling design — one tokenizer, three views, one registry

`MigrationLexer` reads the raw file once, left to right, and at each position outside a token checks the SPEC-007 openers in table order, taking the first match: `--` line comment, `/* */` block comment (nesting counted), `E'…'`, `'…'` (and `U&'`, `B'`, `X'`, `N'` prefixes), `"…"` (and `U&"`), `${…}` placeholder, `$tag$…$tag$` dollar body. A `$` that continues an identifier and `$1` are not dollar quotes. Inside a body only the body's own end and the same inner rules apply; the body end always wins. An opener still open at end of file produces one `LexProblem` on its line, and tokenizing resumes after that single character.

The lexer returns three same-length views (`data-model.md` §1): (a) code text with comments blanked and strings kept, (b) identifier text with comments and strings blanked and quoted identifiers kept, (c) statements as offset ranges over (b), cut only at top-level `;` tokens from the token list, with start line and kind read from (b). Blanked characters become spaces and newlines are kept, so an offset means the same position in every view.

`MigrationRules.all()` returns the 15 rules in one ordered list; adding a rule is one class plus one entry (`SPEC-016`). `LiteralSchemaRule` decides `isAllowedQualifier(MigrationStatement, String)` in one method, returning true only for `${recoverySchema}`, `information_schema` and `pg_catalog`. No `public` exception is built (SEAM-E044-01, owner RWB-E1-069). `ForeignKeyOutsideRule` never consults that method. `GrantRule` reads the code text of a statement; `SearchPathRule` runs on view (a).

Finding multiplicity is enforced in `MigrationFinding`: one finding per (rule, file, line, key). `L-LITERAL-SCHEMA` key: the disallowed schema name as PostgreSQL resolves it; `L-FK-OUTSIDE` key: the referenced qualifier; `L-SEARCH-PATH` and `L-GRANT`: no key (at most one per line); `L-LEX`: the opener offset. `SequenceGapRule` compares the sorted **distinct** sequence numbers against `1..N`, so a duplicate is reported once by `SequenceDuplicateRule` and not also as a gap (PA-E044-06).

### Flyway bean changes

1. **Pin (SPEC-002).** `RecoveryMigrationProperties` carries `@Validated`; `schema` carries `@NotNull` and `@Pattern(regexp = "recovery")`. `MigrationPropertiesConfig` registers it with no condition, so the binding and the validation happen on every start, whatever `rwb.flyway.enabled` is. `@EnableConfigurationProperties` is removed from `RecoveryFlywayConfig`. The record keeps `schema` as its first component and stays the first parameter of `recoveryFlyway`. The message names `rwb.schema` and `D-RCV-28`; Spring's field error adds the rejected value. No credential is in the message.
2. **No check in a constructor** (SPEC-002): building the record in code is unaffected, so RWB-TE-001's direct-call tests need no change (T-044-08 case (6)).
3. **Explicit `validateOnMigrate(true)`** added to the configuration; `ignoreMigrationPatterns` stays at Flyway's `*:future` default (SPEC-001, SPEC-013).
4. **Factory never migrates (SPEC-003).** `recoveryFlyway(RecoveryMigrationProperties, DataSource, DataSourceProperties)` loses `@Bean(initMethod = "migrate")` and only returns `configuration…load()`. A new `@Bean(initMethod = "migrate") RecoveryMigrationRunner recoveryMigrationRunner(Flyway recoveryFlyway, RecoveryMigrationProperties properties)` does the migrate at container initialisation.
5. **Failure report (SPEC-003).** `migrate()` catches `FlywayException`, logs exactly one ERROR line `MSG-P3-016 schema={} object={}` (SLF4J parameterised; no SQL, no credentials), then rethrows, so the context fails. `failureObject` picks `object` as follows, checked against flyway-core **12.4.0** with `javap` on 18 Nov 2026:

   | Failure | Source of `object` | Verified API |
   |---|---|---|
   | Validation failure (checksum mismatch, applied file missing, lower version pending under `outOfOrder(false)`) | Version(s) of the invalid migrations, comma-separated | `flyway.validateWithResult()` → `ValidateResult.invalidMigrations` (`List<ValidateOutput>`, field `version`). The method exists in 12.4.0 and returns the result object, which is why the spec names it; `FlywayValidateException` in this version exposes no invalid list. |
   | Migration that fails part way | Version of the failed migration (first pending after the PostgreSQL rollback) | `flyway.info()` → `MigrationInfoService.pending()`, `MigrationInfo.getVersion()` |
   | No version (connection refused, lock timeout, missing schema) | `recoveryFlyway` | fallback |

   ASM-E044-12 allows another public Flyway call that yields the same version; T-044-09, -12, -13 and -14 are the acceptance. A refused `clean()` is not wrapped (Flyway's own message; DG-L11).
6. **Data source selection, history table, placeholder, `outOfOrder(false)`, `baselineVersion("0")`, `baselineOnMigrate(true)`, `cleanDisabled(true)`, `createSchemas(false)`, `validateMigrationNaming(true)` stay as they are** (Change Scope "Inherited Existing Behavior").

### Container test design (SPEC-011)

One class, `T/casewf/migration/RecoveryMigrationIT.java`, tagged `@Tag("recovery-it")`, so `recoveryIntegrationTest` runs it and it fails (not skips) without Docker.

- Two static `PostgreSQLContainer` fields on `postgres:16.16-alpine`, built as `RecoveryDatabaseIT` does (copy `infra/postgres/init` to `/docker-entrypoint-initdb.d`, copy `infra/postgres/schema` to `/schema`, `RWB_LOAD_REFERENCE_SCHEMA=false`, synthetic passwords, the same wait strategy and timeout). AC2 and AC3 use one database on each container.
- A `newDatabase(String name)` helper connects as the container superuser, runs `CREATE DATABASE <name>`, then `CREATE SCHEMA recovery AUTHORIZATION rwb_migrator` — the state `10-load-ace-database.sh` leaves in `ace` when `RWB_LOAD_REFERENCE_SCHEMA=false` (`infra/postgres/init/10-load-ace-database.sh` lines 31–37). Every case starts from a fresh database so cases cannot leak into each other.
- Flyway is always built through `RecoveryFlywayConfig#recoveryFlyway`: an `ApplicationContextRunner` with `withUserConfiguration(MigrationPropertiesConfig.class, RecoveryFlywayConfig.class)` and a nested `@TestConfiguration` that supplies a `DataSource` (`DriverManagerDataSource` on the migrator URL) and a `DataSourceProperties` bean, because the factory method resolves both parameters even when the `rwb.flyway.user` branch is taken. `rwb.schema=recovery`, `rwb.flyway.url/user/password` select `rwb_migrator`, and only `rwb.flyway.location` is pointed at a fixture folder (`filesystem:` form, so a `@TempDir` copy can be modified).
- Cases that assert a failed start (T-044-12, the lower-version part of T-044-13, T-044-14, T-044-17 (f)) assert on `context.getStartupFailure()` (the `FlywayException` in the cause chain) and on the captured log line. For T-044-17 (f) the test walks the cause chain to the `java.sql.SQLException` and asserts `getSQLState()` is exactly `42501`.
- Log capture: a Logback `ListAppender<ILoggingEvent>` attached to the `RecoveryMigrationRunner` logger, removed in a `finally`. No new dependency (logback-classic is on the test runtime through Spring Boot logging).
- Reads after a migration use plain JDBC (`DriverManager.getConnection`) so no extra Spring bean is created.
- T-044-17 connects as `rwb_migrator` for (e) and (f) and as the superuser for the catalog checks (a)–(d).

### Coverage wiring (SPEC-014, TASK-13)

RWB-TE-001 plan v7 TASK-01 and "Coverage gate edit" show `boundaryToolingClasses` includes only `th/co/scb/ace/demo/recovery/architecture/boundary/**`. **That include does not take in `architecture/migration/**`**, so case 1 of SPEC-014 applies: this story adds its own directory to both tasks. The edit is exactly the one described in the build/infra/docs table; nothing else in the file changes. TASK-00 confirms the case against the merged `build.gradle.kts` and stops and reports on a mismatch (ASM-E044-19).

## Tests

| Level | Test IDs | Where | Gate |
|---|---|---|---|
| Unit (test-scope tooling) | T-044-01..-07, -19, -20, -21, -22 | `T/architecture/RecoveryMigrationLintTest.java`, `T/architecture/migration/MigrationLexerTest.java`, `T/architecture/migration/SchemaComparatorTest.java` | `./gradlew test`; tooling classes measured in the 80% bundle |
| Unit (main code) | T-044-08, -09 | `T/casewf/migration/MigrationPropertiesConfigTest.java`, `T/casewf/migration/RecoveryMigrationRunnerTest.java` | `./gradlew test`; measured in the 80% bundle |
| Container | T-044-10..-18 | `T/casewf/migration/RecoveryMigrationIT.java` (`recovery-it`) | `./scripts/dev.ps1 it`; does not replace unit coverage |

Test-first order and every command are in `tasks.md`. The red runs (TASK-01, -03, -05, -07, -09, -11) are recorded with command, exit code and first failing assertion under `implement/`.

## Functional Test Scenarios

| ID | Scenario | Owner | Assignment | Evidence |
|---|---|---|---|---|
| FTS-E044-01 | A developer adds a non-compliant migration and the build fails with the `MSG-P3-016` lint line naming file and line | Functional Automation Test | **NOT_APPLICABLE** — no UI, no screen, no route; the same check is executed as unit tests T-044-01..-07, -20..-22 in `./gradlew test`, which is not a functional automation result | `implement/unit-tests/report.md` |
| FTS-E044-02 | A deployment applies a pending migration once and a second start applies nothing; the run is visible in `flyway_schema_history_recovery` | API Tester | **NOT_APPLICABLE** — no endpoint. `GET /api/recovery/v1/admin/jobs` is unchanged and its migration-run part is out of scope (D-RCV-12) | T-044-10 container result; no `api-tests/` run is required |
| FTS-E044-03 | The service refuses to start with a wrong `rwb.schema` and with Flyway on or off | Functional Automation Test | **NOT_APPLICABLE** — a start-up configuration behaviour, proven by unit tests T-044-08 in the Spring `ApplicationContextRunner`, not by a UI or API journey | `implement/unit-tests/report.md` |
| HV-E044-01 | The environment owner applies R1 and R2 in SIT, UAT and PROD | Human (recovery tech lead / environment owner) | Not testable here (no target databases); never reported as tested | OI-E044-I, OI-E044-J |

No functional-automation or API-tester execution is planned: the story adds no screen, route or endpoint. This is recorded as `NOT_APPLICABLE` with the scope evidence above, not as an executed test.

## Migrations

**None.** Decision Log v10 D-RCV-28 and story v7 §13 both say RWB-E1-044 "ships no production migration file"; the code already holds the Flyway bean and the lint (audit A-04). No `<seq>` is fixed (D-RUN-07), and `backend/src/main/resources/db/modulemigration/recovery/` stays without a `.sql` file. Every `V<seq>__…` file this plan names is a **test fixture** under `backend/src/test/resources/migration-lint/` or `backend/src/test/resources/flyway-fixtures/` and uses concrete numbers only because the lint checks contiguity from `V0001` (ASM-E044-14). If an implementation ever needs a production migration, it must be named `V<seq>__rwb_e1_044_<name>.sql` with line 1 `-- Story: RWB-E1-044` and no number fixed here; no such need exists in this scope.

## Rule tables and reference sources read

AGENTS.md §3.2 asks that every threshold, limit, timer, queue, role, template and route come from a versioned reference table. This story adds none of those: the schema value is the D-RCV-28 constant `recovery` (a configuration pin, not a reference row), and the only roles it grants or checks are the database roles of ADR-010. The Workbench permission letters named in the out-of-scope rows (RW-PLATADM, RW-DATASTEW, RW-AUDIT) are not implemented or checked here because no endpoint exists. The rules this plan applies are read from:

| Source (name, version) | What it supplies | Applied in |
|---|---|---|
| Decision Log v10, D-RCV-28 (row DL42) | Name pattern, contiguous sequence, one non-fix file per key, fix line, `${recoverySchema}`, schema `recovery`, no production file for E1-044 | SPEC-001, -002, -005, -006, -007; TASK-04, -08, -16 |
| Squad register D-RCV-28 parts (2)–(4) | Literal-schema scope, Testcontainers/JaCoCo tasks, Flyway's own message for a refused clean | SPEC-007, -011, -013, -014; TASK-04, -12, -14 |
| Build log D-RUN-13, D-RUN-14, D-RUN-17, D-RUN-21 | Literals/comments are not schema references; migrator rights; merge order and TE-001 base; one-module reading | SPEC-007, -017; this plan's three cases and one-module check |
| BS-2.1–2.6, BS-4.5, BS-4.6, BS-7.2 | Schema reference, migration naming, Flyway settings, no grant, lint as a unit test, no credential, 80% coverage | TASK-04, -08, -10, -12, -13 |
| Error and Message Standard v4, MSG-P3-016 | Message ID and its `schema` / `object` parameters; text stays out of code | TASK-02, -04, -10 |
| NFR-027, NFR-052 | Rollback by previous tag; credentials outside the repository | TASK-10, -14 |
| Test standards §1–§6 | Levels, `recovery-it`, synthetic data, coverage rules | TASK-01..-15 |
| Physical Schema v6, Section A; ACE Source Views v1 grant block | The RWB-E1-069 seam that this lint rejects (named, not built) | SPEC-016; TASK-16 README |

## Requirement Logic To Task Coverage

`REQ_REF` values are the rows of `../specify/spec.md` "Requirement-to-SPEC Logic Coverage" (28 rows, unchanged, none merged or dropped).

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| AC1 / BR1 / BR5 | 001, 011 | TASK-10, -14 | INHERITED_EXISTING_BEHAVIOR | T-044-10: `V0001` applies once, version and checksum in `flyway_schema_history_recovery`, rerun applies nothing | COVERED |
| AC2 / BR7 / X1 | 012 | TASK-05, -06, -14 | DIRECT_IMPLEMENTATION | T-044-15 (one difference `recovery.queue.note_x`), T-044-19 (comparator) | COVERED |
| AC2 / BR7 (real SIT/UAT/PROD; read-only account) | 017 | TASK-19 | OUT_OF_SCOPE_BY_DECISION (D-RCV-05) | TASK-19 checks no drift flag, no read-only account and no real-environment code was added | COVERED |
| AC3 / BR2 | 001, 002, 007, 011 | TASK-08, -14 | DIRECT_IMPLEMENTATION | T-044-11 (two databases, `recovery.timer`, equal checksums), T-044-08 case (5) | COVERED |
| AC4 / BR5 / X2 | 001, 003, 011 | TASK-10, -14 | DIRECT_IMPLEMENTATION | T-044-12 (changed file: ERROR line names the version, context fails), T-044-09 | COVERED |
| AC5 / BR2 / X3 | 004, 007, 010 | TASK-03, -04 | DIRECT_IMPLEMENTATION | T-044-02, T-044-06 (format, line 2 for `CREATE INDEX … ON recovery.queue`) | COVERED |
| AC6 / BR3 / X4 | 004, 006, 010 | TASK-03, -04 | DIRECT_IMPLEMENTATION | T-044-03 (`L-KEY-DUP` names both files and `RWB-E1-028`) | COVERED |
| AC7 / BR4 / X5 | 001, 005, 011, 013 | TASK-04, -10, -14 | INHERITED_EXISTING_BEHAVIOR | T-044-13 (`clean()` refused with Flyway's message, object count unchanged), T-044-04 (`L-UNDO`) | COVERED |
| AC8 / X6 | 003, 011 | TASK-10, -14 | DIRECT_IMPLEMENTATION | T-044-14 (first statement rolled back, no history row, ERROR names the version, context fails) | COVERED |
| AC8 (job monitor display) | 017 | TASK-19 | OUT_OF_SCOPE_BY_DECISION (D-RCV-12) | TASK-19 checks no `MigrationRunRecorder`, no job-monitor endpoint or screen was added | COVERED |
| AC9 / X7 | 011 | TASK-14 | INHERITED_EXISTING_BEHAVIOR | T-044-16 (concurrent migrate, one history row, both start) | COVERED |
| BR6 | 001 | TASK-08, -10 | INHERITED_EXISTING_BEHAVIOR | `HISTORY_TABLE` constant unchanged; T-044-10 reads that table; `RecoveryFlywayConfigTest` history-table assertion stays green | COVERED |
| BR8 | 008, 010 | TASK-03, -04, -11, -12 | DIRECT_IMPLEMENTATION | T-044-05 (`L-FK-OUTSIDE` + `L-LITERAL-SCHEMA`, `pg_catalog` gives one) and T-044-17 (f) (SQLSTATE 42501, no history row) | COVERED |
| D-RCV-28 (1) | 005, 006 | TASK-03, -04 | INHERITED_EXISTING_BEHAVIOR | T-044-01, T-044-03 (duplicate seq, multi key line, fix without base, `L-UNDO`) | COVERED |
| D-RCV-28 (2) | 007 | TASK-02, -03, -04 | DIRECT_IMPLEMENTATION | T-044-02, T-044-20, T-044-21, T-044-22 (all forms; statement view S1) | COVERED |
| Decision Log v10 D-RCV-28; story v7 §13 (schema `recovery`) | 002 | TASK-07, -08 | DIRECT_IMPLEMENTATION | T-044-08 cases (1)–(6): wrong, blank, null, relaxed binding, Flyway on and off; direct construction unaffected | COVERED |
| D-RUN-13 | 007, 008 | TASK-02, -03, -04 | DIRECT_IMPLEMENTATION | T-044-21 (literals, doubled quotes, `E'…'`, trailing and multi-line comments pass) and T-044-22 (adversarial) | COVERED |
| D-RCV-48 | 001, 011 | TASK-14 | INHERITED_EXISTING_BEHAVIOR | T-044-18 (non-empty `recovery`, no history table: baseline row 0 then `V0001`) | COVERED |
| NFR-027 | 013 | TASK-10, -14 | DIRECT_IMPLEMENTATION | T-044-13 (previous tag starts; lower pending version fails with its version); `*:future` default kept | COVERED |
| NFR-052 / BS-4.5 | 001 | TASK-08, -10 | INHERITED_EXISTING_BEHAVIOR | No credential in code, config, fixture or log line; T-044-09 asserts the ERROR line holds only the ID and two parameters | COVERED |
| Story §10: pipeline migration account | 001 | TASK-10 | INHERITED_EXISTING_BEHAVIOR | `rwb.flyway.user`/`password` branch unchanged; T-044-09 covers both data-source branches | COVERED |
| Story §10: RW-PLATADM runs deployments | 017 | TASK-19 | OUT_OF_SCOPE_BY_DECISION (pipeline action) | TASK-19 checks no endpoint or role check was added; AGENTS §3.3 applies to endpoints and none exists | COVERED |
| Story §10: read and rerun a migration run; RW-DATASTEW, RW-AUDIT | 017 | TASK-19 | OUT_OF_SCOPE_BY_DECISION (D-RCV-12) | TASK-19 checks no run-read or rerun authority was added; DG-L10, OI-E044-G | COVERED |
| Story §12 `GET /admin/jobs?type=MIGRATION`, `MigrationRunRecorder`, §14 MSG-P4-002, §15 SCR-44, §16 TC-E1-044-10 | 017 | TASK-19 | OUT_OF_SCOPE_BY_DECISION (D-RCV-12) | TASK-19 diff check: no endpoint, recorder, screen or new `MSG-P4-002` use | COVERED |
| Story §14 MSG-P3-016 | 003, 004, 012, 013 | TASK-02, -04, -10 | DIRECT_IMPLEMENTATION | `MigrationFinding.format()` and the runner's ERROR line hold the ID and parameters only (T-044-06, T-044-09); refused clean uses Flyway's message (T-044-13) | COVERED |
| Audit A-19 | 015 | TASK-16 | DIRECT_IMPLEMENTATION | `docs/stories/RWB-E1-044/story.md` and `plan.md` exist and match the README and this plan | COVERED |
| ADR v3 ADR-010; D-RCV-35 U4; Env v4 §5 (Section A views seam) | 016 | TASK-04, -16, -19 | DIRECT_IMPLEMENTATION | `LiteralSchemaRule.isAllowedQualifier` is the only decision point; the seam-marker fixture T-044-02 fails with `L-LITERAL-SCHEMA`; TASK-19 checks no `public` exception was built | COVERED |
| RWB-E1-069 v7 §3 (ACE DBA role, attributed to E1-044) | 017 | TASK-11, -12 | DIRECT_IMPLEMENTATION | T-044-17 (a)–(f): R1 only `USAGE`, R2 `INHERIT FALSE, SET TRUE`, no table privilege, FK refused with 42501; no DBA role | COVERED |

No row is `BLOCKED`.

**Coverage type note.** The five rows marked `OUT_OF_SCOPE_BY_DECISION` are the spec rows that D-RCV-12 (job-monitor parts), D-RCV-05 (real-environment drift), the pipeline-action line and the declined ACE DBA role settle. The planning gate allows `DIRECT_IMPLEMENTATION` or `INHERITED_EXISTING_BEHAVIOR`; neither is true for work another decision removed from this story. The rows are kept visible with their real status, and TASK-19 checks that none of the excluded work was built — the same treatment RWB-TE-001's gated plan gave its moved-out-of-scope row.

## SPEC to task map

| SPEC | Tasks | Tests |
|---|---|---|
| 001 | TASK-08, -10, -14 | T-044-09, -10, -12, -13, -18 |
| 002 | TASK-07, -08 | T-044-08 (cases 1–6), T-044-11 |
| 003 | TASK-09, -10 | T-044-09, -12, -14 |
| 004 | TASK-02, -03, -04 | T-044-01..-07, -20..-22 |
| 005 | TASK-03, -04 | T-044-01, -04 |
| 006 | TASK-03, -04 | T-044-03 |
| 007 | TASK-01, -02, -03, -04 | T-044-02, -20, -21, -22 |
| 008 | TASK-03, -04 | T-044-05, -21, -22 |
| 009 | TASK-03, -04 | T-044-20 |
| 010 | TASK-03, -04 | T-044-01..-07, production-folder test |
| 011 | TASK-11, -12, -14, -15 | T-044-10..-18 |
| 012 | TASK-05, -06, -14 | T-044-15, -19 |
| 013 | TASK-10, -14 | T-044-13 |
| 014 | TASK-13, -17 | `recoveryCoverageVerification` evidence |
| 015 | TASK-16 | review of README and story/plan files |
| 016 | TASK-02, -04, -19 | T-044-02 (seam-marker fixture); scope check |
| 017 | TASK-11, -12, -19 | T-044-17; scope check |

No orphan: every SPEC 001–017 has at least one task.

## Screen-to-task mapping

`NOT_APPLICABLE`: UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`, no effective-screen node and no `SCR-*` screen in the spec. `SCR-44` is out of scope (D-RCV-12). No screen consolidation task is required; the pre-submit check in `tasks.md` records this.

## Security, privacy and compliance

- **Authentication and authorisation.** No endpoint is added or changed (`NO_API_CHANGE`), so no method-security check applies. The job-monitor read and rerun authority, TC-E1-044-10 and `MSG-P4-002` stay out of scope (D-RCV-12; DG-L10; OI-E044-G).
- **Database privilege boundary.** D-RUN-14's two rights are the whole grant: `USAGE` on `public`, no table privilege, and a non-inheriting `ace_view_owner` membership that only allows `SET ROLE` (T-044-17 (a)–(d)). BR8 is enforced twice: the lint in every environment (`L-FK-OUTSIDE`) and the database in this repository (T-044-17 (f), SQLSTATE 42501). The residual `SET ROLE` path is recorded for the tech lead (OI-E044-J); no lint rule here refuses `SET ROLE`.
- **Personal data.** None. Fixtures use synthetic table and column names and the story ACs' names (`queue`, `timer`, `note_x`, `team_code`); the `public.account` reference in T-044-05 and T-044-17 is a table name, not data. No real customer name, ID, account number or address appears in code, fixtures, logs or this plan.
- **Secrets.** Migrator credentials come from the environment or key store; the container test uses synthetic passwords as container environment (`it-migrator`, `it-recovery`), as `RecoveryDatabaseIT` does today. No secret is read from `.env` by any test this story adds.
- **Logging.** The bean's own ERROR line holds only `MSG-P3-016`, `schema` and `object`. The rethrown Flyway exception carries the failing SQL statement (DDL and reference data only; never personal data) and the JDBC URL without a password, and is accepted, not redacted (SPEC-003). Audit A-07 log masking is RWB-TE-011's and is not built here.
- **Audit.** No case or decision changes; the migration record is the history table plus the ERROR line (ASM-E044-02). KYC/AML, suitability and approval are not in scope.

## Release and rollback

- **Release:** no runtime feature flag; the change is a build-time lint plus start-up behaviour (NFR-027; story v7 §13). `rwb.flyway.enabled=false` remains an inherited operational switch and still cannot bypass the schema pin.
- **Release note item (for the deployer):** any environment that sets `RWB_SCHEMA` to a value other than `recovery` now fails at start with the configuration error. That is the intended D-RCV-28 behaviour; remove the variable. `RWB_FLYWAY_ENABLED=false` does not avoid it.
- **Rollback:** redeploy the previous tag. `outOfOrder(false)` and the `*:future` default mean the previous tag starts against a database that already holds a later version and applies nothing (T-044-13). `clean` stays disabled in every environment; no undo file exists (`L-UNDO`).
- **Merge:** the orchestrator merges into `develop-recovery` only after `./scripts/dev.ps1 test` exits 0 on the branch and `./scripts/dev.ps1 it` exits 0 (D-RCV-44). `recoveryCoverageVerification` is shown separately at the code gate (R3-3 of RWB-TE-001's plan).
- **Wave A order (D-RUN-17):** RWB-TE-001 merges first; this story's code gate runs after it. The plan is written now against TE-001's gated plan, as D-RUN-17 permits.

Nothing in this plan, `tasks.md` or the supporting files claims a human approval. `PLANNER_CLARIFICATION_STATUS` is ready, and the plan gate is the orchestrator's to run.

## Assumptions

Plan-stage assumptions are in `assumptions.md` (PA-E044-01..PA-E044-14). Spec assumptions ASM-E044-01..-19 are carried unchanged and are not re-litigated here.

## Status

```text
PLANNER_STATUS_SUMMARY: Plan ready: 20 tasks (TASK-00..TASK-19) for the migration lint tooling and fixtures, the schema pin, the MSG-P3-016 failure report, the D-RUN-14 migrator rights, the container proof, the coverage addition and the documentation conventions.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: spec v14-7 passed the gate; RWB-TE-001 plan v7 gated and used as the base; every SPEC, AC and BR mapped to tasks and named tests] [UNBLOCK_ACTION: n/a]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO; no screen, route or component changes]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: All 28 requirement-logic rows, SPEC-001 to SPEC-017, AC1 to AC9 and BR1 to BR8 map to tasks and named tests; the out-of-scope rows are mapped to TASK-19 as recorded exclusions.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 28] [TASK_COVERED_RULES: 28] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
GATE_REVIEW: PENDING_ORCHESTRATOR
```
