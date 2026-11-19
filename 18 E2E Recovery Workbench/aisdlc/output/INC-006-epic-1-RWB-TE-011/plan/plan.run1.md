---
title: "Implementation Plan: RWB-TE-011 PDPA lint for code, tests and logs"
run_id: "INC-006-epic-1-RWB-TE-011"
story: "RWB-TE-011"
epic: "EPIC-001"
status: "SUCCESS"
revision: "v1 (18 Nov 2026): first plan for this repository, written against spec run 12 (spec gate round 13 PASS 0C/0H/0M/0L)."
prepared: "2026-11-18"
---

# Implementation Plan: RWB-TE-011 PDPA lint for code, tests and logs

Design Source: `NOT_REQUIRED` (UI In Scope: NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` in spec.md). No `frontend/components.md` is created.

| Field | Value |
|---|---|
| Spec | `../specify/spec.md` (remediation run 12, 1,314 lines; SPEC-TE011-001..018). Spec gate round 13: `PASS` 0/0/0/0 (`../review/spec-gate-review-13.md`). `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 32] [MISSING_RULES: 0] [CONTRADICTIONS: 0]`. |
| Change type | `NEW_STORY`. `UI In Scope: NO`, `API Impact: NO_API_CHANGE`, `Logic In Scope: YES`. New build tooling under `tools/pdpa-lint/`, one CI job, one `scripts/dev.ps1` command, one code-owner line. |
| Code base | This repository on `develop-recovery` at commit `8675a5c`, as read on 18 Nov 2026. No code, git state or shared file is changed by this stage. |
| Builder | Implementation Builder in its own worktree on `feature/RWB-TE-011-pdpa-lint` from `develop-recovery`, after RWB-TE-001, RWB-E1-044, RWB-E1-042, RWB-TE-002 and RWB-TE-003 are merged. Evidence goes to `aisdlc/output/INC-006-epic-1-RWB-TE-011/implement/`. |
| Smallest change | One standalone Gradle project under `tools/pdpa-lint/` (35 main classes, 31 test files, fixture trees, two configuration files), one new `.gitlab-ci.yml` job, one new `scripts/dev.ps1` command plus the lint step in `test`, one line in `.gitlab/CODEOWNERS`, two `.gitignore` lines. No application code, no endpoint, no migration, no frontend file. |
| Migration | **None.** D-RUN-07 is not exercised. This story creates no `V<seq>__rwb_te_011_*.sql`; the corrective-migration rule of SPEC-TE011-018 is lint logic, not a script. TASK-34 checks the diff. |
| One-module check | PASS under D-RUN-21. No file under `th.co.scb.ace.demo.recovery` or under any other ACE module is created or changed. The change is repository-level build tooling, pipeline and code-owner governance around the recovery module. No `common/` or `collection/` file is touched (see "One-module check"). |

## Upstream readiness

| Check | Result |
|---|---|
| Spec gate | `PASS` round 13, 0 Critical, 0 High, 0 Medium, 0 Low (`spec-gate-review-13.md` §1, §5). No new document gap; no earlier finding reopened. |
| Spec status signal | The spec `Status` row records the round-12 remediation and names round 13 as next; `spec-gate-review-13.md` closes the gate and says "the plan gate may start". `REQUIREMENT_COVERAGE_RESULT: SUCCESS` is present. The literal `Status: SUCCESS` line that `implementation-execution-gates.md` wants before build is absent from `spec.md`; the gate `PASS` plus the coverage result is the "equivalent ready state" of `planning-execution-gates.md`. TASK-00 stops if the spec header still lacks an approved status at build time (SU-TE011-01 asks the orchestrator to set it; no human approval is claimed here). |
| Clarification log | CLAR-001..CLAR-015 all `RESOLVED`; `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]` (`spec.md` "Clarification Log"). Carried into tasks in "Carried clarifications" below. |
| Requirement coverage | 32 of 32 rows of the spec "Requirement-to-SPEC Logic Coverage" table map to tasks and to a named verification; none is `BLOCKED`. |
| Design evidence | `NOT_REQUIRED` (UI In Scope NO): no screen task, no screen-to-task mapping, no consolidation task, no `frontend/components.md`. |
| Dependencies | Only earlier stories in Build Sequence v6: RWB-E1-044 (order 1), RWB-TE-001 (order 2), RWB-E1-042 (order 3), RWB-TE-002 (order 4), RWB-TE-003 (order 5). Later work is a named seam only (D-RUN-08): RWB-E1-001 (order 9), RWB-E1-043 (order 8), RWB-E1-064 (order 13), RWB-E1-065 (order 14). |
| Migration | None. D-RUN-07 not exercised. |

`PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]`. The shared open items named by the spec (`OPEN-038`, `OPEN-024`, RWB-E1-043 R4, and the proposed `OPEN-NEW-TE011-*`) are not `CLAR-*` items and none blocks planning.

**Build decisions applied.** D-RUN-07: no migration number is fixed and this story adds no migration. D-RUN-08: later work (RWB-E1-001, -043, -064, -065) is a named seam only. D-RUN-17: RWB-TE-001 merges before RWB-E1-044, so both are preconditions of this story and TASK-00 checks them. D-RUN-19: the parameter-read interface in P4 `access.api` is unchanged and not used by the tool; no P1, P2 or P4 to P3 edge is created. D-RUN-21: "touches one module" is read as the ACE module (recovery); this plan changes no module file at all. D-RUN-15: A-07 (raw exception text, `traceId`) belongs to RWB-TE-003 and is out of scope. None of these is ratified as a human decision here; OPEN-050 stays open.

## Carried clarifications

Every resolved clarification is connected to the work it controls. "Spec" is `../specify/spec.md`.

| CLAR | Decision carried | SPEC | TASK | Verification |
|---|---|---|---|---|
| CLAR-001 | Field list is the dictionary as seeded and changed by migrations plus the API marks; classification stays with Compliance (DL26) | 001, 016 | TASK-07, TASK-33 | UT-TE011-10, ST-TE011-11, TASK-33 limit statement |
| CLAR-002 | Masking helper list is configuration, empty in production; AC8 proven with a test configuration | 010 | TASK-15, TASK-31 | UT-TE011-21, ST-TE011-08 |
| CLAR-003 | Example domains, mobile forms and the check-digit algorithm are configured, labelled defaults | 009, 015 | TASK-21, TASK-03 | UT-TE011-31..33, UT-TE011-01 |
| CLAR-004 | Non-text personal fields accept no literal; outside the migration folder an allow entry is the only exception | 008 | TASK-17, TASK-23 | UT-TE011-27, UT-TE011-35 |
| CLAR-005 | Entity names are generated with configured suffixes (default `Entity`, `View`) | 002, 005 | TASK-09, TASK-15 | UT-TE011-11, UT-TE011-18 |
| CLAR-006 | The national ID is generated at run time into a temp fixture; no value is stored | 009 | TASK-21 | UT-TE011-31, ST-TE011-03 |
| CLAR-007 | The code-owner line is added to `[Recovery module]`; TC-TE-011-11 is `BLOCKED` locally | 014 | TASK-31 | UT-TE011-43, HV-01 |
| CLAR-008 | A finding prints the dictionary name and, when different, the matched token in parentheses | 012 | TASK-29 | UT-TE011-40, ST-TE011-01 |
| CLAR-009 | Fixtures match by (object, field); unresolved positions use the unambiguous-name rule and API personal names | 001, 002, 008, 011, 016 | TASK-07..11, TASK-17, TASK-19 | UT-TE011-05..13, UT-TE011-27..30, ST-TE011-11..15 |
| CLAR-010 | The lint covers committed SQL, fixtures and logs only; a load mark is outside it (RWB-E1-064 seam, R4) | 001, 016, 017 | TASK-07, TASK-34 | UT-TE011-10, TASK-33/34 limit statement |
| CLAR-011 | API personal names are always findings in API-typed positions (protective reading of DGL-15) | 002, 008 | TASK-09, TASK-19 | UT-TE011-11, UT-TE011-30, ST-TE011-14 |
| CLAR-012 | Corrective migration under the original story key is the only remedy; unrecognised SQL fails closed | 008, 016, 017, 018 | TASK-17, TASK-27, TASK-33 | UT-TE011-22..26, UT-TE011-38/39, ST-TE011-16 |
| CLAR-013 | No configuration may exclude or omit the migration folder; exclusions are printed with counts | 003, 012, 015 | TASK-11, TASK-29 | UT-TE011-12/13, UT-TE011-40, ST-TE011-18 |
| CLAR-014 | A code-owner-reviewed lint-fixture class (`backend/src/test/resources/migration-lint/**`) gets FIXTURE-ID only | 003, 008, 016, 018 | TASK-11, TASK-27, TASK-33 | UT-TE011-12/13, ST-TE011-18, TASK-33 |
| CLAR-015 | The changed-file list is built from git against `develop-recovery` locally and `origin/<target>` in GitLab | 003, 013, 018 | TASK-25, TASK-31 | UT-TE011-36/37, ST-TE011-19, UT-TE011-43 |

## Plan inputs (read only)

Shorthands used below and in `tasks.md`: `P` = `tools/pdpa-lint`, `M` = `P/src/main/java/th/co/scb/ace/tools/pdpa`, `U` = `P/src/test/java/th/co/scb/ace/tools/pdpa`, `X` = `P/src/test/resources`.

| Path | Read for |
|---|---|
| `aisdlc/output/INC-006-epic-1-RWB-TE-011/specify/spec.md` | The approved specification, 1,314 lines |
| `.../specify/assumptions.md` | ASM-TE011-01..29 |
| `.../specify/document-gaps.md` | DGL-01..15, all Blocker = No |
| `.../specify/shared-updates.md` | Proposed open items and the §3b note to earlier planners |
| `.../specify/contracts/backend-apis.json`, `frontend-integrations.json` | `NO_API_CHANGE`; build-tool contract; frontend `NOT_APPLICABLE` |
| `.../review/spec-gate-review-13.md` | Gate result, the duplicate-pipeline note for the plan |
| `aisdlc/output/INC-002-epic-1-RWB-TE-001/plan/plan.md` (v7), `tasks.md` (v7), `data-model.md`, `tests/scenarios.md` | Package layout, tooling test conventions, coverage-gate wiring, evidence conventions |
| `aisdlc/output/INC-001-epic-1-RWB-E1-044/plan/data-model.md` §3 and `specify/spec.md` (v14-7) | Lint-fixture corpus under `backend/src/test/resources/migration-lint/`; Flyway fixtures |
| `aisdlc/output/INC-004-epic-1-RWB-TE-002/plan/plan.md` (v2) | `.gitlab/CODEOWNERS` section format and validator V4/V7/V9 |
| `.gitlab-ci.yml` | 53 lines; stages `verify`, `integration`; three jobs; `eclipse-temurin:21-jdk`; flow-style maps |
| `scripts/dev.ps1` | 123 lines; `ValidateSet`; `test` = `gradlew test` then `npm run check`; `Invoke-Native` exit-code handling |
| `backend/build.gradle.kts`, `backend/settings.gradle.kts` | 160 lines; JaCoCo tasks; toolchain 21; project dir `backend/` |
| `backend/gradle/wrapper/gradle-wrapper.properties` | Gradle 9.9.1 |
| `backend/src/main/resources/application.yaml` | `rwb.flyway.location: classpath:db/modulemigration/recovery` at line 83 |
| `backend/src/main/resources/db/modulemigration/recovery/README.md` | The folder holds only this file today |
| `infra/postgres/schema/03-recovery-physical-schema-v6.sql` | The dictionary stand-in: 1,379 `INSERT INTO sys_fields` rows, named columns |
| `api/recovery-api-v4.yaml` | 5 `x-personal-data: true` properties |
| `.gitignore`, `.editorconfig`, `.gitattributes` | Build output is not ignored for `tools/`; Java tabs; YAML two spaces; `ps1` CRLF |
| `AGENTS.md` §3, §4, §6, §7, §9; `README.md`; `AI-SDLC-BUILD-LOG.md` decisions | Guardrails, one-module rule, merge gate, D-RUN-06/07/08/15/17/19/21 |
| `aisdlc/.github/rules/*` and `aisdlc/.github/contexts/*` | Plan structure, coverage gate, testing standards, coding standards |

## Plan-time verification (read only)

| Item | Method | Result (18 Nov 2026) |
|---|---|---|
| Branch and head | `git rev-parse --abbrev-ref HEAD`, `git log --oneline -1` | `develop-recovery`, `8675a5c` |
| Tool folder | `Test-Path tools`, `Test-Path .gitlab` | Both absent; RWB-TE-002 and this story have not run |
| Git availability | `git --version` | 2.53.0; the temporary-repository tests need it |
| Parser and test libraries | `./gradlew --offline -q dependencies --configuration runtimeClasspath` and `testRuntimeClasspath` in `backend/` | `org.yaml:snakeyaml:2.6`; `tools.jackson.core:jackson-core:3.1.7`; `org.junit.jupiter:junit-jupiter:6.0.3`; `org.assertj:assertj-core:3.27.7`. All are already resolved by the backend build; this plan approves and pins them for the tool under BS-1.5 |
| Gradle wrapper | `gradle-wrapper.properties` | Gradle 9.9.1, so `backend/gradlew -p tools/pdpa-lint` runs the tool project with no new wrapper |
| Dictionary input | Count of `INSERT INTO sys_fields` in the Physical Schema v6 copy | 1,379; every row names its columns |
| API marks | Count of `x-personal-data: true` in `api/recovery-api-v4.yaml` | 5 |
| Migration folder | File listing | Only `README.md`; no `.sql` file today |
| Test resources | File listing of `backend/src/test/resources` | Empty; RWB-E1-044 and RWB-TE-001 have not merged |
| Backend log calls | Spec preflight evidence, re-read source | 4 calls today (`ApiExceptionHandler` 2, `DroolsRuleEngine` 1, `TemporalConfig` 1); none uses a personal field |
| Local pipeline image | `.gitlab-ci.yml` | `eclipse-temurin:21-jdk`; `git` is not guaranteed in that image, so the job installs it (PA-TE011-09) |
| Coverage tool | `backend/build.gradle.kts` | JaCoCo plugin present; the tool project declares its own JaCoCo tasks |
| Glob semantics | A five-line Java `PathMatcher` check run on 18 Nov 2026 | Java's `glob:...recovery/**/*.java` returns false for `recovery/package-info.java`; the tool therefore implements Git-style `**` (zero or more segments), so the top-level migration and `package-info.java` are matched (PA-TE011-25, UT-TE011-12) |

## Preconditions from earlier stories

TASK-00 confirms each on the worktree base and stops if one is absent. This plan builds none of them.

| Story (order) | What this plan expects | If absent or different |
|---|---|---|
| RWB-TE-001 (2) | The 19 module packages and relocated classes; `RecoveryFlywayConfig` in `casewf/migration`; `backend/build.gradle.kts` with the TE-001 JaCoCo edits | Stop; the scan root `backend/src/main/java/th/co/scb/ace/demo/recovery/**` still works, but the preflight cannot confirm D-RUN-17 |
| RWB-E1-044 (1) | `backend/src/test/resources/migration-lint/**` (the lint-fixture corpus, including `notes.txt` and `README.md`) and `backend/src/test/resources/flyway-fixtures/**` | Stop and report; the default `lintFixtureRoots` and the "known files" reading of SPEC-TE011-003 depend on them |
| RWB-E1-042 (3) | The one production migration of orders 1–5, with its `INSERT … ON CONFLICT DO NOTHING`, `INSERT … SELECT … WHERE NOT EXISTS` and its 16 guarded constraint additions | Record each merged file and scan it at TASK-33; a finding is handled by SPEC-TE011-018, never by an allow entry |
| RWB-TE-002 (4) | `.gitlab/CODEOWNERS` with section `[Recovery module]`, and `.gitlab/codeowners-register.yaml` with the TechX handle; its validator tests read the real file | Stop; the code-owner line of SPEC-TE011-014 has no home, and TC-TE-011-11 stays `BLOCKED` |
| RWB-TE-003 (5) | `ContractFixtures` test source and no new SQL | Nothing to scan; record it |
| All five | `./scripts/dev.ps1 test` exits 0 on the base before any change | Record the baseline; a red base is reported, not fixed by this story |

## Scope

Each bullet maps to tasks in `tasks.md` ("Scope bullet to task map").

1. **S-1 Tool project, build, configuration and CLI** (SPEC-TE011-013, -015): standalone Gradle project at `P`, the two reviewed configuration files, the CLI and the exit-code entry point. → TASK-01, TASK-03.
2. **S-2 Dictionary reader** (SPEC-TE011-001): form R1, form R2, the ignored class, the fail-closed class, order rules, notices, point-in-time snapshots and the API union. → TASK-04, TASK-05, TASK-06, TASK-07.
3. **S-3 Rule generator and `pdpa-rules.yaml`** (SPEC-TE011-002): variants, entity names, keys, ambiguity and API names, deterministic. → TASK-08, TASK-09.
4. **S-4 Scan scope** (SPEC-TE011-003): roots, classes, exclusions, lint-fixture class, migration-folder probes, `rwb.flyway.location`, counts. → TASK-10, TASK-11.
5. **S-5 Source lexing and type index** (SPEC-TE011-004..-007): Java and TypeScript tokens, strings, text blocks, template literals, declarations, `@Table`, `schema.d.ts`. → TASK-12, TASK-13.
6. **S-6 Log, entity, exception and text-form rules, masking exemption** (SPEC-TE011-004, -005, -006, -007, -010). → TASK-14, TASK-15.
7. **S-7 SQL statement classes and SQL fixture positions** (SPEC-TE011-008): classes 1–4, `(columns not named)`, `(statement not recognised)`, `(DML in procedural body)`, `DEFAULT`, `EXECUTE` and `format`. → TASK-16, TASK-17.
8. **S-8 Java, TypeScript and JSON fixture positions** (SPEC-TE011-008): setters, builders, assignments, object literals, `fixtureObjects`, resolution and the name rule. → TASK-18, TASK-19.
9. **S-9 FIXTURE-ID matchers** (SPEC-TE011-009): check digit, mobile forms and example domains, all on raw text, values never printed. → TASK-20, TASK-21.
10. **S-10 Allow list** (SPEC-TE011-011): schema, expiry, pattern and line, and the migration-folder prohibition. → TASK-22, TASK-23.
11. **S-11 Changed-file list** (SPEC-TE011-013, -018(e)): decision before any git call, merge base, `AMR` filter, and every exit-2 case. → TASK-24, TASK-25.
12. **S-12 Output, exit codes, determinism and `PdpaLintStep`** (SPEC-TE011-012): sorting, notices, counts, scope lines, exit 0/1/2, no value ever printed. → TASK-28, TASK-29.
13. **S-13 Corrective-migration recognition** (SPEC-TE011-018): line-2 naming, conditions (a)–(e), target tables per finding kind, unknown file, C scanned. → TASK-26, TASK-27.
14. **S-14 Pipeline job, local gate and code owners** (SPEC-TE011-013, -014): `.gitlab-ci.yml` job, `scripts/dev.ps1` (`test` step and `pdpa-lint` command), the `.gitlab/CODEOWNERS` line. → TASK-30, TASK-31.
15. **S-15 System evidence, baseline pass, coverage, negative controls and guardrails** (SPEC-TE011-016, -017): TC and TS fixture trees, 80% × 4 coverage, the real-repository run, the merge-gate negative controls and the scope check. → TASK-32, TASK-33, TASK-34.

Out of scope (SPEC-TE011-017 "Out of scope"; unchanged): secret scanning, dependency approval, ZAP, Playwright or axe jobs; the contract job (RWB-TE-003); `ApiExceptionHandler` raw exception text and the Problem `traceId` (RWB-TE-003, D-RUN-15); publishing the masking helper (common module, OPEN-024); writing the CODEOWNERS file and branch rules (RWB-TE-002); protecting `is_personal` on a dictionary load and the load handler (RWB-E1-064; decision in RWB-E1-043 open item R4, owned by RW-COMPLY); policing run-time loads; aligning the API `x-personal-data` marks (OPEN-NEW-TE011-8); reading a database; seeding the protective classification (RWB-E1-001). Each is a named seam owned by a later story and is not built.

## One-module check

`AGENTS.md` §7 and §9 ask that a plan touch one module. Under build decision **D-RUN-21** (build log, 18 Nov 2026 05:36, the orchestrator, Claude Code), "module" means the ACE module, the recovery module. This plan passes on the stronger reading too: it creates or changes **no** file under `th.co.scb.ace.demo.recovery` or any other Java package of the service. The touched areas are `tools/` (a standalone build tool), `.gitlab/` (repository governance), `scripts/` (the local entry point), `.gitlab-ci.yml` and `.gitignore`. No `common/` or `collection/` file is touched. OPEN-050 keeps D-RUN-18..D-RUN-21 pending tech-lead ratification; this plan records that and claims no approval.

## Backend Plan

Surface status: **CHANGED — build tooling only**. Unit tests **REQUIRED**: JaCoCo LINE, BRANCH, METHOD and INSTRUCTION at `0.80` on every `P/src/main` class, by `jacocoTestCoverageVerification` in the tool's own Gradle project. No change to `backend/src/main`, `backend/build.gradle.kts`, `backend/settings.gradle.kts`, any endpoint, entity, migration or runtime configuration.

### Tool files (exact paths)

Every file below is added. `P`, `M`, `U`, `X` are the shorthands above.

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Add | `P/settings.gradle.kts` | TASK-01 | 013 |
| Add | `P/build.gradle.kts` | TASK-01 | 013, 016 |
| Add | `P/pdpa-lint.yaml` | TASK-01 | 015 |
| Add | `P/pdpa-allow.yaml` | TASK-01 | 011, 015 |
| Add | `P/README.md` | TASK-01 | 013, 015 |
| Add | `M/PdpaLint.java` (main, CLI to exit code) | TASK-01, TASK-29 | 012, 013 |
| Add | `M/PdpaLintStep.java` (reader to report) | TASK-01, TASK-29 | 012 |
| Add | `M/cli/CliOptions.java` | TASK-01, TASK-03 | 013, 015 |
| Add | `M/config/LintConfig.java` (records for every configuration section) | TASK-01, TASK-03 | 015 |
| Add | `M/config/ConfigLoader.java` | TASK-01, TASK-03 | 015 |
| Add | `M/config/RepositoryLayout.java` (`rwb.flyway.location`, path resolution) | TASK-01, TASK-03 | 003, 015 |
| Add | `M/dictionary/Dictionary.java` (fields, by-name, described pairs, snapshots, API names) | TASK-01, TASK-07 | 001, 002, 008 |
| Add | `M/dictionary/PersonalField.java` (record) | TASK-01, TASK-07 | 001 |
| Add | `M/dictionary/PersonalFieldReader.java` (R1, R2, ignored, fail closed, order) | TASK-01, TASK-07 | 001 |
| Add | `M/dictionary/ApiSpecificationReader.java` | TASK-01, TASK-07 | 001 |
| Add | `M/dictionary/RuleGenerator.java` | TASK-01, TASK-09 | 002 |
| Add | `M/sql/SqlStatement.java` (text, start line, offsets) | TASK-01, TASK-05 | 001, 008 |
| Add | `M/sql/SqlSplitter.java` (quote-aware lexer and splitter) | TASK-01, TASK-05 | 001, 008 |
| Add | `M/sql/SqlTarget.java` (table, column, literal flags) | TASK-01, TASK-17 | 018 |
| Add | `M/sql/SqlValueSlot.java` (target, span, DEFAULT flag) | TASK-01, TASK-17 | 008, 018 |
| Add | `M/scan/ScanScope.java` (roots, classes, exclusions, lint fixtures, probes, walk, counts) | TASK-01, TASK-11 | 003 |
| Add | `M/scan/ScannedFile.java` | TASK-01, TASK-11 | 003 |
| Add | `M/scan/SourceLexer.java` (Java and TypeScript) | TASK-01, TASK-13 | 004..007 |
| Add | `M/scan/SourceIndex.java` (declarations, types, `@Table`, `schema.d.ts`) | TASK-01, TASK-13 | 004..007 |
| Add | `M/scan/LogScanner.java` (LOG-FIELD, LOG-ENTITY, EXCEPTION, TOSTRING, masking) | TASK-01, TASK-15 | 004..007, 010 |
| Add | `M/scan/SqlFixtureScanner.java` (classes 1–4, positions, columns not named, slots) | TASK-01, TASK-17 | 008, 018 |
| Add | `M/scan/FixturePositionScanner.java` (Java and TypeScript positions) | TASK-01, TASK-19 | 008 |
| Add | `M/scan/JsonFixtureScanner.java` (`fixtureObjects`) | TASK-01, TASK-19 | 008 |
| Add | `M/scan/FixtureIdMatcher.java` (three matchers) | TASK-01, TASK-21 | 009 |
| Add | `M/scan/CorrectiveMigrations.java` (line-2 naming and conditions (a)–(e)) | TASK-01, TASK-27 | 018 |
| Add | `M/scan/Finding.java` | TASK-01, TASK-29 | 012 |
| Add | `M/scan/Notice.java` | TASK-01, TASK-29 | 012 |
| Add | `M/scan/Rule.java` (the six rule IDs) | TASK-01, TASK-29 | 002, 012 |
| Add | `M/allow/AllowList.java` | TASK-01, TASK-23 | 011 |
| Add | `M/allow/AllowEntry.java` | TASK-01, TASK-23 | 011 |
| Add | `M/changes/ChangedFileList.java` | TASK-01, TASK-25 | 013, 018 |
| Add | `M/changes/GitRunner.java` (interface) | TASK-01, TASK-25 | 013 |
| Add | `M/changes/ProcessGitRunner.java` | TASK-01, TASK-25 | 013 |
| Add | `M/report/Report.java` (sorting, lines, counts, scope lines, exit code) | TASK-01, TASK-29 | 012 |
| Add | `M/report/RulesFileWriter.java` | TASK-01, TASK-09 | 002 |

Test files (all added):

| Kind | Path | Task | Covers |
|---|---|---|---|
| Add | `U/LintHarness.java` (temp tree, config rewrite, captured output, no-value assertion) | TASK-28 | ST-01..19 |
| Add | `U/TestValues.java` (test dictionary and run-time-built failing values) | TASK-20, TASK-28 | UT-31..34; every ST |
| Add | `U/TestRepository.java` (temporary git repository) | TASK-24 | UT-36, UT-37, ST-19 |
| Add | `U/config/ConfigLoaderTest.java` | TASK-02 | UT-01, UT-02 |
| Add | `U/config/RepositoryLayoutTest.java` | TASK-02 | UT-03 |
| Add | `U/sql/SqlSplitterTest.java` | TASK-04 | UT-04 |
| Add | `U/dictionary/PersonalFieldReaderTest.java` | TASK-06 | UT-05..UT-10 |
| Add | `U/dictionary/ApiSpecificationReaderTest.java` | TASK-06 | UT-10 |
| Add | `U/dictionary/RuleGeneratorTest.java` | TASK-08 | UT-11 |
| Add | `U/scan/ScanScopeTest.java` | TASK-10 | UT-12, UT-13 |
| Add | `U/scan/SourceLexerTest.java` | TASK-12 | UT-14 |
| Add | `U/scan/SourceIndexTest.java` | TASK-12 | UT-15 |
| Add | `U/scan/LogScannerTest.java` | TASK-14 | UT-16..UT-21 |
| Add | `U/scan/SqlFixtureScannerTest.java` | TASK-16 | UT-22..UT-28 |
| Add | `U/scan/FixturePositionScannerTest.java` | TASK-18 | UT-29 |
| Add | `U/scan/JsonFixtureScannerTest.java` | TASK-18 | UT-30 |
| Add | `U/scan/FixtureIdMatcherTest.java` | TASK-20 | UT-31..UT-34 |
| Add | `U/scan/CorrectiveMigrationsTest.java` | TASK-26 | UT-38, UT-39 |
| Add | `U/allow/AllowListTest.java` | TASK-22 | UT-35 |
| Add | `U/changes/ChangedFileListTest.java` | TASK-24 | UT-36, UT-37 |
| Add | `U/report/ReportTest.java` | TASK-28 | UT-40 |
| Add | `U/report/RulesFileWriterTest.java` | TASK-08 | UT-11 |
| Add | `U/PdpaLintStepTest.java` | TASK-28 | UT-41 |
| Add | `U/system/LogAndExceptionSystemTest.java` | TASK-28 | ST-01, -02, -07, -08, -09, -10 |
| Add | `U/system/FixtureSystemTest.java` | TASK-28 | ST-03, -04, -06, -12..-15 |
| Add | `U/system/DictionarySystemTest.java` | TASK-28 | ST-05, -11 |
| Add | `U/system/SqlClassSystemTest.java` | TASK-28 | ST-17 |
| Add | `U/system/LintFixtureSystemTest.java` | TASK-28 | ST-18 |
| Add | `U/system/CorrectiveMigrationSystemTest.java` | TASK-28 | ST-16 |
| Add | `U/system/ChangedFileSystemTest.java` | TASK-28 | ST-19 |
| Add | `U/system/RepositoryConfigTest.java` | TASK-30 | UT-43 |

Fixture trees are listed in `data-model.md` §7; every file is under `X/trees/`. No fixture stores a value that matches a FIXTURE-ID pattern; such values are built at run time (SPEC-TE011-009, -016).

Repository and shared files (exact paths):

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Edit | `scripts/dev.ps1` (add `pdpa-lint` to `ValidateSet`, add `Invoke-PdpaLint`, add the step to `test`) | TASK-31 | 013 |
| Edit | `.gitlab-ci.yml` (add job `pdpa-lint` after `frontend-check`) | TASK-31 | 013 |
| Edit | `.gitlab/CODEOWNERS` (one line in section `[Recovery module]`) | TASK-31 | 014 |
| Edit | `.gitignore` (`tools/pdpa-lint/build/`, `tools/pdpa-lint/.gradle/`) | TASK-01 | 015 |
| Evidence | `aisdlc/output/INC-006-epic-1-RWB-TE-011/implement/**` | TASK-00, -32, -33, -34 | 016, 017 |

Not changed: any file under `backend/src/main/java`, `backend/src/main/resources`, `backend/src/test/**` (other than reading), `frontend/**`, `api/**`, `infra/**`; `backend/build.gradle.kts`; `backend/settings.gradle.kts`; `.env.example`; `AGENTS.md`; `README.md`.

### Configuration files

`P/pdpa-lint.yaml` and `P/pdpa-allow.yaml` are data, reviewed by code owners. The production `pdpa-allow.yaml` is an empty list: no finding exists on 18 Nov 2026 that needs an entry (spec state (1)). The full key set, defaults and the exact production content are in `data-model.md` §3 and §4. No **personal** field name or **personal** object name, and no prefix, example domain or matcher pattern, is written in code (SPEC-TE011-015); the metadata identifiers `sys_fields` and its columns are the reader's rule vocabulary. The matcher implementations are the rule (SPEC-TE011-009), the names, enablement, example domains and `fixtureObjects` are configuration.

### Build, coverage and commands

- The tool is a standalone Gradle project (`P/settings.gradle.kts`: `rootProject.name = "pdpa-lint"`). It is run through the existing wrapper: from the repository root, `./backend/gradlew -p tools/pdpa-lint <tasks>`. No wrapper binary is added to `P`.
- Java 21 toolchain, the same compiler level as `backend/build.gradle.kts`. `application` plugin with `mainClass = "th.co.scb.ace.tools.pdpa.PdpaLint"`.
- Dependencies, pinned: `org.yaml:snakeyaml:2.6` (YAML input and the allow list), `tools.jackson.core:jackson-core:3.1.7` (JSON fixture streaming with line numbers), test `org.junit.jupiter:junit-jupiter:6.0.3` and `org.assertj:assertj-core:3.27.7`, plus `org.junit.platform:junit-platform-launcher:6.0.3` at test runtime. All are the versions the backend already resolves; no other dependency. This is the BS-1.5 plan approval.
- Tasks: `test` (JUnit 5, `useJUnitPlatform()`), `jacocoTestReport` (`finalizedBy` from `test`), `jacocoTestCoverageVerification` (LINE, BRANCH, METHOD, INSTRUCTION each `0.80`), and `check` depends on `jacocoTestCoverageVerification`. `test` working directory is the repository root so repository-relative paths and `Path.of("")` work.
- `pdpaLint` is a `JavaExec` task with `workingDir` = repository root, main class above, and two optional Gradle properties `pdpaLint.changedFrom` and `pdpaLint.branch` that become `--changed-files-from-git <from> --branch <branch>`; when absent, neither option is passed. Gradle's `JavaExec` failure on exit 1 or 2 fails the Gradle build; the tool's own line states the reason.
- CLI options (SPEC-TE011-013 fixes the last two): `--repo-root <dir>` (default `.`), `--config <file>` (default `tools/pdpa-lint/pdpa-lint.yaml`), `--rules-out <file>` (default `tools/pdpa-lint/build/pdpa-rules.yaml`), `--run-date <YYYY-MM-DD>` (default today in Asia/Bangkok), `--changed-files-from-git <target>`, `--branch <name>`. The first four are plan additions needed for tests and for the build-output rule; the spec's two are implemented exactly.
- `pdpa-rules.yaml` is written before scanning, after the dictionary is complete, and is not committed (`build/` is ignored). A run that fails while reading the dictionary writes no rules file.

### Pipeline and local gate

`data-model.md` §6 holds the exact job text and `data-model.md` §8 the exact `dev.ps1` block. In short:

- The job `pdpa-lint` is in stage `verify`, image `eclipse-temurin:21-jdk`, `GIT_DEPTH: "0"`, Gradle cache as the other jobs, `rules:` for `merge_request_event`, `$CI_COMMIT_BRANCH` and `$CI_COMMIT_TAG`, and a `before_script` that installs `git` only if the image lacks it. It runs `clean check` then `pdpaLint` under `set -o pipefail`, tees the console to `P/build/pdpa-lint-console.log`, and keeps `pdpa-rules.yaml`, the console log, the JaCoCo report and the JUnit XML as artifacts (`when: always`).
- Tag pipeline: no changed-file option, no fetch. Branch pipeline: delete `refs/remotes/origin/<target>`, non-fatal fetch, pass `origin/<target> --branch $CI_COMMIT_BRANCH`. Merge request pipeline: the same delete-then-fetch with `origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME --branch $CI_MERGE_REQUEST_SOURCE_BRANCH_NAME`. `PDPA_LINT_TARGET_BRANCH` reproduces the default `changedFiles.targetBranch`, and UT-TE011-43 fails if the two differ.
- `scripts/dev.ps1`: `pdpa-lint` joins `ValidateSet`; `Invoke-PdpaLint` resolves the current branch with `git -C $Root rev-parse --abbrev-ref HEAD` and runs `backend\gradlew.bat -p tools\pdpa-lint pdpaLint -PpdpaLint.changedFrom=develop-recovery -PpdpaLint.branch=<branch>`; `test` runs the backend Gradle tests, then `check pdpaLint` for the tool, then `npm run check`.
- **Duplicate pipelines (observation carried from spec gate round 12/13).** A push to an open merge request's source branch produces a branch pipeline and a merge request pipeline, and `pdpa-lint` runs in both. That follows GitLab's documented duplicate-pipeline behaviour and the three rules the spec requires; the cost is one extra lint run per push. It is recorded as risk R-1, not as a defect.

### Behaviour preserved (no semantic loss)

The plan adds no rule, relaxes no rule and moves no value to code. The exact value-level logic is kept in the tasks and tests:

- Reader forms R1 and R2, the ignored class and the fail-closed class with its exit-2 text; baseline replacement, duplicate detection, unknown `field_id`, point-in-time snapshots, the unmarking notice, `is_active` ignored (SPEC-TE011-001).
- The six rule IDs and their exact finding text; the field/token parenthesis form; four notice kinds; four counts; scope lines; exit 0/1/2 (SPEC-TE011-012).
- The three fixture-ID patterns with the check-digit formula, the national, international and bare-country-code mobile forms, the example domains and reserved TLDs; every failing value built at run time (SPEC-TE011-009).
- The allow entry schema with `rule`, `path`, `line` xor `pattern`, `owner`, `reason`, `expires`; Asia/Bangkok inclusive expiry; expired-used adds the expired line; expired-unused passes; any entry matching the migration folder is invalid (SPEC-TE011-011).
- SQL classes 1–4 with the listed tails, `DEFAULT` positions, `(columns not named)`, `(statement not recognised)`, `(DML in procedural body)`, `%I` versus `%s`/`%L`, `%%`, and the placeholder `DEFAULT` cases (SPEC-TE011-008).
- Corrective conditions (a)–(e) and the target table per finding kind, including the table-only rule for a placeholder column and the no-acceptance rule for a placeholder table (SPEC-TE011-018).
- The changed-file decision before any git command, and the three exit-2 texts; no fallback to an empty list (SPEC-TE011-013).

## Frontend Plan

Surface status: **NOT_APPLICABLE** for implementation and unit tests.

Evidence: spec "Frontend Specification" records `Changes required: NO`; `UI In Scope: NO` and `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`; no screen, route, state, component, service, label or i18n key is added; no file under `frontend/` is added or changed. Front-end source and tests are **scan input** for SPEC-TE011-003 (the TypeScript log rules of SPEC-TE011-004 and the TypeScript fixture positions of SPEC-TE011-008 are exercised inside the tool's own test suite with `.ts`/`.tsx` fixtures). `frontend/e2e/platform.spec.ts` holds three addresses in the reserved `.test` domain and passes unchanged. TASK-34 checks `git diff --stat` on `frontend/` is empty. The unchanged front-end regression (`npm run check`, Vitest 80% thresholds in `frontend/vite.config.ts`) still runs inside `./scripts/dev.ps1 test` (TASK-33).

`frontend/components.md` is **not created**: UI In Scope NO. `NOT_APPLICABLE`.

## Unit test applicability

| Surface | Changes required | Unit tests | Coverage gate | Trace | Evidence and reason |
|---|---|---|---|---|---|
| Backend | YES (build tooling `P`; application code unchanged) | REQUIRED | JaCoCo LINE, BRANCH, METHOD, INSTRUCTION each >= 0.80 on every `P/src/main` class, by `jacocoTestCoverageVerification`; native XML and HTML reports | SPEC-TE011-001..-018; BR1–BR7; AC1–AC10 | New hand-written logic with branches in a new project (spec "Unit Test Applicability"). Tests: TASK-02..TASK-30. Results: TASK-32. |
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE (metrics `N/A`) | SPEC-TE011-003 (scan input only) | No frontend change (spec "Frontend Specification"); TypeScript rule behaviour is covered by the backend (tool) row. |

The final evidence follows `implementation-execution-gates.md`: one row per surface in `implement/unit-tests/report.md`, with the backend row populated from `P/build/reports/jacoco/test/jacocoTestReport.xml` and the frontend row `NOT_APPLICABLE` with the spec/plan rationale and `N/A` metrics.

## Rule tables and migrations read

- Migration scripts written: **none**. D-RUN-07 is not exercised. `backend/src/main/resources/db/modulemigration/recovery/` gains no file from this story.
- Rule and reference data read by the tool: `sys_fields` (columns `field_id`, `object_name`, `field_name`, `data_type`, `source_field`, `is_personal`, `is_active`) from `infra/postgres/schema/03-recovery-physical-schema-v6.sql` and from `sys_fields` statements in the recovery migration folder; `x-personal-data` from `api/recovery-api-v4.yaml`; the repository configuration files `P/pdpa-lint.yaml` and `P/pdpa-allow.yaml`; `rwb.flyway.location` from `backend/src/main/resources/application.yaml`.
- No threshold, timer, queue, role, template or route is written as a literal: the synthetic prefix, example domains, matcher enablement, logger names, exception types, masking helpers, entity suffixes, `fixtureObjects`, `lintFixtureRoots`, `changedFiles` and the scan roots are configuration (AGENTS.md §3.2, §4.8). The governance route for the two tool configuration files is `.gitlab/CODEOWNERS` (SPEC-TE011-014).
- The lint's own rule IDs (`PDPA-*`) and output text are the story's rule vocabulary, not business values (SPEC-TE011-012).
- No case, stage, milestone, sentry or decision-log entry: this story changes no case and takes no decision (AGENTS.md §3.4 not exercised).

## Test strategy, harness and fixture trees

- Two levels, both in the tool's `test` task: **unit tests** `UT-TE011-01..43` against one component or one classifier table, and **system tests** `ST-TE011-01..19` running the full lint (reader, generator, scope, scanners, allow list, corrective rules, report) over a temporary tree; `ST-TE011-20` is the recorded real-repository run of TASK-33. `tests/scenarios.md` names every case and its expected output; `data-model.md` §7 lists every fixture file.
- `LintHarness` copies a tree from `X/trees/<name>/` into `@TempDir`, copies the real `api/recovery-api-v4.yaml` beside it, writes `tools/pdpa-lint/pdpa-lint.yaml` by loading the real configuration and replacing only `dictionary`, `api`, `allowList`, `fixtures.fixtureObjects` and `changedFiles`, writes the default synthetic test dictionary unless the tree supplies `dictionary/baseline.sql`, runs `PdpaLintStep`, and returns the exit code and the ordered output lines. Every system test asserts that no fixture value appears in the output (BR7).
- Failing values (valid national ID with check digit, Thai mobile in each form, an address outside the example domains) are assembled by `TestValues` with a fixed seed at run time. They are never stored in the repository; the tool's self-scan (FIXTURE-ID only under `P`) fails the build if one is stored.
- `TestRepository` builds temporary git repositories for the changed-file tests: an initial `develop-recovery` branch, a feature branch, an orphan branch, a depth-1 clone and a stale `refs/remotes/origin/develop-recovery` working copy.
- No test is skipped, disabled or weakened. No `@Disabled`, `@Ignore`, assumption or conditional skip is used. A test that needs `git` or a real repository file fails loudly if it is missing.
- The real-repository run is **evidence, not a unit test** (TASK-33): a permanent test asserting zero findings on the working tree would fail for another story's merged migration and would be red for reasons this story does not own. `UT-TE011-10` reads the real Physical Schema v6 copy and asserts 18 personal fields; `UT-TE011-03` reads the real `application.yaml`; `UT-TE011-43` reads the real `.gitlab-ci.yml` and `.gitlab/CODEOWNERS`.
- State (1) of SPEC-TE011-016 is this story's merge condition and TASK-33 records it. State (2) is RWB-E1-001's merge condition, when its migration replaces the baseline rows with the protective union; state (3) is every later merge. The TASK-33 report names the state the repository is in and repeats the residual-risk limit beside the result.

## Execution order (tests before code, AGENTS.md rules 3 and 10)

1. **TASK-00** pre-flight; stop on a failed precondition.
2. **TASK-01** project, type skeletons (signatures only, no logic), configuration files and `.gitignore`; the coverage task is red at 0%.
3. Red/green pairs in dependency order: **02/03** config, **04/05** SQL splitter, **06/07** reader and API union, **08/09** generator, **10/11** scope, **12/13** source lexer and index, **14/15** log and text-form rules, **16/17** SQL classes and positions, **18/19** Java, TypeScript and JSON positions, **20/21** fixture IDs, **22/23** allow list, **24/25** changed-file list, **26/27** corrective migrations, **28/29** output and step with the system tests.
4. **30/31** repository files: CI job, `dev.ps1`, code-owner line, and the configuration test that reads them.
5. **32** full suite and coverage evidence; **33** real-repository baseline and merge-gate negative controls; **34** scope, guardrail and evidence check.

Every red run is recorded in `implement/` with the command, the exit code and the first failing assertion; every green run with the final summary line and the coverage counters. TASK-01's skeleton exists so that each red task fails by assertion, not by compilation (the lesson of RWB-TE-001 plan finding PLAN-015).

## Functional Test Scenarios

The story has no screen and no endpoint. The full-lint scenarios are JVM system tests in the tool's suite; the host behaviour is human verification and is never reported as tested.

| ID | Scenario | Assigned to | Scope and evidence |
|---|---|---|---|
| FTS-01 | AC1–AC10 end to end over fixture trees: Java and TypeScript log calls, whole entities, exception messages, text forms, fixture fields, national ID, allow expiry, masking helper | Implementation Builder (tool system tests) | ST-TE011-01..10 in `U/system/*`; run by `test` inside `./scripts/dev.ps1 test`; evidence `implement/backend/tool-test.log` |
| FTS-02 | Additional full-lint scenarios TS-TE011-01..09: dictionary seeds, point in time, source-field key, unresolved objects, columns not named, corrective migration, SQL classes, lint fixtures, changed-file list | Implementation Builder (tool system tests) | ST-TE011-11..19; same run and log |
| FTS-03 | The real repository in state (1) of SPEC-TE011-016: 0 findings, 0 exit-2 errors, the notice and scope lines, and every file merged by orders 1–5 listed with its result | Implementation Builder (recorded run) | TASK-33; `implement/baseline-run.log` and `implement/baseline-files.md`; the residual-risk limit repeated beside the result |
| FTS-04 | The local merge gate: `./scripts/dev.ps1 test` green on the branch, then red with a planted fixture-ID value and red with a planted non-synthetic personal-field literal, then green again | Implementation Builder (recorded runs) | TASK-33; three runs with exit codes in `implement/merge-gate.md` |
| API scenarios | None | API Tester | `NOT_APPLICABLE`: `NO_API_CHANGE`, no endpoint, no schema (`contracts/backend-apis.json`) |
| UI and user-workflow scenarios | None | Functional Automation Test | `NOT_APPLICABLE`: no screen, route or component (UI In Scope NO); the TypeScript rules are system-tested with `.ts`/`.tsx` fixtures in the tool suite |
| HV | Host behaviour: MR pipeline exists for every MR and blocks on a red `pdpa-lint`; a non-code-owner approval is refused; branch fetch and `GIT_DEPTH: 0` on the runner; the ACE pipeline copy | Human verification on the GitLab/ACE host (owner: ACE platform with the recovery tech lead) | HV-01..HV-04, each `OPEN — NOT_TESTED_HERE`; TC-TE-011-11 is `BLOCKED`, never passed |

## Requirement Logic To Task Coverage

`REQ_REF` values are the 32 rows of the spec "Requirement-to-SPEC Logic Coverage" table. "ST/UT" are the scenario IDs of `tests/scenarios.md`; "HV" is human verification. All rows are `COVERED`; none is `BLOCKED`.

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| SRC-01 §4.1 | SPEC-001 | TASK-05, TASK-07 | DIRECT_IMPLEMENTATION | UT-TE011-05..10; ST-TE011-11, ST-20 | COVERED |
| SRC-01 §4.2 | SPEC-002 | TASK-09 | DIRECT_IMPLEMENTATION | UT-TE011-11; ST-TE011-05 | COVERED |
| SRC-01 §4.3 | SPEC-003, -004, -005, -006 | TASK-11, TASK-13, TASK-15 | DIRECT_IMPLEMENTATION | UT-TE011-12..19; ST-TE011-01, -02, -07, -09 | COVERED |
| SRC-01 §4.4 | SPEC-003, -008, -009 | TASK-11, TASK-17, TASK-19, TASK-21 | DIRECT_IMPLEMENTATION | UT-TE011-22..34; ST-TE011-03, -04, -12..-15, -17, -18 | COVERED |
| SRC-01 §4.5 | SPEC-007 | TASK-15 | DIRECT_IMPLEMENTATION | UT-TE011-20; ST-TE011-10 | COVERED |
| SRC-01 §4.6 | SPEC-011 | TASK-23 | DIRECT_IMPLEMENTATION | UT-TE011-35; ST-TE011-06 | COVERED |
| SRC-01 §4.7 | SPEC-012, -013 | TASK-29, TASK-31 | DIRECT_IMPLEMENTATION | UT-TE011-40; all ST assert no value; UT-TE011-43 | COVERED |
| BR1 | SPEC-001, -002, -015 | TASK-01, TASK-03, TASK-07, TASK-09 | DIRECT_IMPLEMENTATION | UT-TE011-01, UT-TE011-05..11 | COVERED |
| BR2 | SPEC-004, -005, -006 | TASK-15 | DIRECT_IMPLEMENTATION | UT-TE011-16..19; ST-TE011-01, -02, -07, -09 | COVERED |
| BR3 | SPEC-008 | TASK-17, TASK-19 | DIRECT_IMPLEMENTATION | UT-TE011-27..30; ST-TE011-04, -14, -15 | COVERED |
| BR4 | SPEC-009 | TASK-21 | DIRECT_IMPLEMENTATION | UT-TE011-31..34; ST-TE011-03 | COVERED |
| BR5 | SPEC-007 | TASK-15 | DIRECT_IMPLEMENTATION | UT-TE011-20; ST-TE011-10 | COVERED |
| BR6 | SPEC-011 | TASK-23 | DIRECT_IMPLEMENTATION | UT-TE011-35; ST-TE011-06 | COVERED |
| BR7 | SPEC-012 | TASK-29 | DIRECT_IMPLEMENTATION | UT-TE011-40; every ST asserts no value | COVERED |
| X1–X11 | SPEC-004..-014 | TASK-15, TASK-21, TASK-23, TASK-27, TASK-29, TASK-31 | DIRECT_IMPLEMENTATION | UT-TE011-16, UT-TE011-31..35, UT-TE011-38/39, UT-TE011-40; HV-01 | COVERED |
| AC1–AC10 | SPEC-004..-011 | TASK-15, TASK-17, TASK-19, TASK-21, TASK-23 | DIRECT_IMPLEMENTATION | ST-TE011-01..10 | COVERED |
| SRC-01 §10 | SPEC-014 | TASK-31 | DIRECT_IMPLEMENTATION | UT-TE011-43; HV-01 | COVERED |
| SRC-01 §12 Trigger | SPEC-013 | TASK-31 | DIRECT_IMPLEMENTATION | UT-TE011-43; HV-02 | COVERED |
| SRC-01 §12 Idempotency / Restart | SPEC-002, -012 | TASK-09, TASK-29 | DIRECT_IMPLEMENTATION | UT-TE011-11, UT-TE011-40 | COVERED |
| SRC-01 §13 Configuration | SPEC-015 | TASK-01, TASK-03 | DIRECT_IMPLEMENTATION | UT-TE011-01..03 | COVERED |
| SRC-01 §13 Done when | SPEC-016, -017 | TASK-06, TASK-07, TASK-32, TASK-33 | DIRECT_IMPLEMENTATION | ST-TE011-11, ST-TE011-20; UT-TE011-05..10; TASK-33 | COVERED |
| SRC-01 §11 Data | SPEC-001, -016, -017 | TASK-07, TASK-33 | DIRECT_IMPLEMENTATION | UT-TE011-10; ST-TE011-11; ST-TE011-20 | COVERED |
| SRC-01 §13 Feature flag | SPEC-013 | TASK-34 | INHERITED_EXISTING_BEHAVIOR | TASK-34 check: no flag, no runtime path | COVERED |
| SRC-01 §17 | SPEC-001, -009, -011, -015 | TASK-01, TASK-03, TASK-21, TASK-23, TASK-34 | DIRECT_IMPLEMENTATION | UT-TE011-01, UT-TE011-31..35; TASK-34 | COVERED |
| REQ-RDF-010 | SPEC-008, -009, -011, -014 | TASK-17, TASK-19, TASK-21, TASK-23, TASK-31 | DIRECT_IMPLEMENTATION | UT-TE011-27..35; UT-TE011-43 | COVERED |
| REQ-ACA-005 | SPEC-004..-007, -010 | TASK-15 | DIRECT_IMPLEMENTATION | UT-TE011-16..21; ST-TE011-01, -02, -07..-10 | COVERED |
| NFR-054 (PDPA part) | SPEC-013 | TASK-31 | DIRECT_IMPLEMENTATION | UT-TE011-43; HV-02 | COVERED |
| NFR-045 | SPEC-008, -009 | TASK-17, TASK-19, TASK-21 | DIRECT_IMPLEMENTATION | UT-TE011-24..34 | COVERED |
| CTL-11 | SPEC-004..-007 | TASK-15 | DIRECT_IMPLEMENTATION | UT-TE011-16..21 | COVERED |
| SRC-19 A-09 (PDPA part) | SPEC-013 | TASK-31 | DIRECT_IMPLEMENTATION | UT-TE011-43; HV-02 | COVERED |
| D-RCV-28; `AGENTS.md` §3.7, §4.6 | SPEC-003, -008, -011, -013, -018 | TASK-11, TASK-17, TASK-23, TASK-25, TASK-27 | DIRECT_IMPLEMENTATION | UT-TE011-13, UT-TE011-35..39; ST-TE011-16, ST-TE011-19 | COVERED |
| DL v10 D-RCV-29 | SPEC-001, -017 | TASK-07, TASK-34 | DIRECT_IMPLEMENTATION | UT-TE011-10; TASK-34 limit statement | COVERED |

## SPEC to task map

| SPEC | Tasks | Tests and verification |
|---|---|---|
| SPEC-TE011-001 | TASK-05, TASK-07 | UT-TE011-04..10 |
| SPEC-TE011-002 | TASK-09 | UT-TE011-11, ST-TE011-05 |
| SPEC-TE011-003 | TASK-11, TASK-19, TASK-27, TASK-31 | UT-TE011-12, UT-TE011-13, UT-TE011-30, UT-TE011-43, ST-TE011-18 |
| SPEC-TE011-004 | TASK-15 | UT-TE011-16, UT-TE011-17, ST-TE011-01, ST-TE011-07 |
| SPEC-TE011-005 | TASK-15 | UT-TE011-18, ST-TE011-02 |
| SPEC-TE011-006 | TASK-15 | UT-TE011-19, ST-TE011-09 |
| SPEC-TE011-007 | TASK-15 | UT-TE011-20, ST-TE011-10 |
| SPEC-TE011-008 | TASK-17, TASK-19 | UT-TE011-22..30, ST-TE011-04, ST-TE011-13..15, ST-TE011-17 |
| SPEC-TE011-009 | TASK-21 | UT-TE011-31..34, ST-TE011-03 |
| SPEC-TE011-010 | TASK-15 | UT-TE011-21, ST-TE011-08 |
| SPEC-TE011-011 | TASK-23 | UT-TE011-35, ST-TE011-06 |
| SPEC-TE011-012 | TASK-29 | UT-TE011-40, all ST |
| SPEC-TE011-013 | TASK-25, TASK-31 | UT-TE011-36, UT-TE011-37, UT-TE011-43, ST-TE011-19 |
| SPEC-TE011-014 | TASK-31 | UT-TE011-43, HV-01 |
| SPEC-TE011-015 | TASK-01, TASK-03 | UT-TE011-01..03 |
| SPEC-TE011-016 | TASK-07, TASK-28, TASK-33 | UT-TE011-10, ST-TE011-11, ST-TE011-20, TASK-33 |
| SPEC-TE011-017 | TASK-00, TASK-33, TASK-34 | TASK-00 checklist, TASK-33 evidence, TASK-34 limits |
| SPEC-TE011-018 | TASK-27 | UT-TE011-38, UT-TE011-39, ST-TE011-16 |

No orphan SPEC; no task without a SPEC (see `tasks.md` "Pre-submit checks").

## Screen-to-task mapping

`NOT_APPLICABLE`: UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`, no effective-screen node and no `SCR-*` screen in the spec. No screen consolidation task is required; the pre-submit check records this.

## Security, privacy and compliance

- **No personal data in the repository, tests, fixtures or logs.** All test values are synthetic and built at run time where they would otherwise match a FIXTURE-ID pattern. The tool's output never contains a value, a source line or SQL text (BR7); every system test asserts this. The evidence files record field names, file paths, line numbers, rule IDs and counts only.
- **No secret.** The tool reads no credential and calls no network. The CI job uses the existing Gradle cache; no new secret or variable holding a secret is added. `PDPA_LINT_TARGET_BRANCH` and `GIT_DEPTH` are non-secret configuration.
- **No authority at run time.** The story adds no endpoint and no Spring Security check (AGENTS.md §3.3 not exercised); authority over `P/pdpa-lint.yaml`, `P/pdpa-allow.yaml` and the rule generator is change control through `.gitlab/CODEOWNERS` (SPEC-TE011-014), verified by UT-TE011-43 and host item HV-01.
- **No audit, KYC, AML, suitability or approval behaviour.** The lint changes no case and takes no business decision (SRC-01 §9); AGENTS.md §3.4 is not exercised.
- **Privacy control.** This is the build-time control for REQ-RDF-010, REQ-ACA-005 and CTL-11 (NFR-054 PDPA part): it blocks personal data in code, fixtures and logs. Its limit is stated wherever the result is reported: it covers the dictionary as seeded and changed by migrations, not marks that arrive only by a D-RCV-29 dictionary load (DGL-13; the RWB-E1-064 seam and RWB-E1-043 open item R4, owned by RW-COMPLY).
- **Guardrails.** Every failing-value test generates its value; no such value is stored. No allow entry exists in production. No finding is excused by an exclusion or by weakening a rule. TASK-34 checks each.
- **Checks.** TASK-34 and the TASK-33 negative controls.

## Release and rollback

No feature flag: a build check has no runtime path (SRC-01 §13). Rollback is a revert merge request of `P`, the `pdpa-lint` job, the `dev.ps1` block, the code-owner line and the two `.gitignore` lines. The orchestrator merges into `develop-recovery` only after `./scripts/dev.ps1 test` exits 0 on the branch (D-RUN-06) and the plan and code gates pass. The `pdpa-lint` job is the merge gate in GitLab and the local `test` command is the gate for the orchestrator's local merge; both run the same tool. In ACE the same job is wired into the ACE pipeline on the `develop-recovery` merge request by the ACE platform (D-RCV-50), which is host work (HV-03).

## Risks

| ID | Risk | Control |
|---|---|---|
| R-1 | A push to an open merge request produces a branch pipeline and a merge request pipeline, so `pdpa-lint` runs twice (spec gate round 12/13 observation). | Accepted: the three `rules:` are what the spec requires, and the duplicate run costs time only. Recorded, not treated as a defect. |
| R-2 | The `eclipse-temurin:21-jdk` image may not carry `git`, so the changed-file list cannot run. | The job installs `git` only when absent; the tool treats a missing or failing git as exit 2 where the list is built and never falls back to an empty list (PA-TE011-09). |
| R-3 | A merged migration of orders 1–5 has a finding; this story's merge request cannot go green. | Recorded by TASK-33 with file, line, rule and field; the orchestrator assigns a corrective migration to the owning story (SPEC-TE011-018); no allow entry and no exclusion is used. This story does not edit another story's file. |
| R-4 | RWB-E1-044's Flyway fixture for AC8 is written as a column-less `INSERT` with a literal, giving a `(columns not named)` finding. | TASK-00 records the merged form; TASK-33 reports it. The route is the reviewed configuration change of SPEC-TE011-003 ("If a merged Flyway fixture gives a finding") or a corrective migration if it is a migration; nothing is asked of RWB-E1-044. |
| R-5 | The 80% branch gate on a lexer-heavy tool is hard to reach. | Tests are written per branch table (UT-TE011-14, UT-TE011-22..26) and the system tests add coverage; the Builder adds tests, never an exclusion or a lower threshold. |
| R-6 | Under the protective union the dictionary marks 526 fields; a scanner that is too eager produces many findings on existing tests. | The plan implements the exact (object, field) rule and the unresolved-name rule; ST-TE011-11 exercises the union shape and ST-TE011-20 records the real result and the residual limit. The dictionary today is the 18-field baseline. |
| R-7 | Windows path separators and CRLF reach glob matching or line numbers. | Scan paths are normalised to `/`; files are read as UTF-8 with `\r` stripped for scanning; UT-TE011-12 and UT-TE011-40 run on Windows and in Linux CI. |
| R-8 | The tool's `build/` is scanned by the self-scan and generated files give findings. | `**/build/**` and `**/coverage/**` are exclusions; the `PDPA-SCOPE:` lines print their counts (UT-TE011-12, UT-TE011-40). |
| R-9 | `PDPA_LINT_TARGET_BRANCH` and `changedFiles.targetBranch` drift apart. | UT-TE011-43 fails when they differ. |

## Document gaps

`document-gaps.md`: PG-TE011-01..05, all Blocker = No, plus the carried DGL-01..15 (none reopened). No gap blocks planning; no document-set source is edited.

## Assumptions

`assumptions.md`: PA-TE011-01..25, plus the carried spec assumptions ASM-TE011-01..29 unchanged. No question was asked (L-RCV-03; RUN-BRIEF rule 4).

## Status

```text
PLANNER_STATUS_SUMMARY: Plan ready: 35 tasks (TASK-00..TASK-34) for a standalone PDPA lint tool, its fixtures, the GitLab job, the local gate and the code-owner line; 10 built-in system test cases plus 9 added system scenarios and 43 unit test groups.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: spec gate round 13 PASS 0/0/0/0; CLAR-001..015 resolved; 32/32 spec coverage rows mapped; every SPEC mapped to tasks and named tests] [UNBLOCK_ACTION: n/a for planning; build needs the five earlier stories merged, per TASK-00]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO; DESIGN_EVIDENCE_STATUS NOT_REQUIRED]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: AC1-AC10, BR1-BR7, X1-X11, T1-T15 and the five upstream requirements map to tasks and named tests; TC-TE-011-11 stays BLOCKED for the host and HV-01.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 32] [TASK_COVERED_RULES: 32] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
FRONTEND_UNIT_TESTS: NOT_APPLICABLE [REASON: no frontend file changes; front-end source is scan input]
BACKEND_UNIT_TESTS: REQUIRED [GATE: 80% LINE/BRANCH/METHOD/INSTRUCTION on tools/pdpa-lint main classes via jacocoTestCoverageVerification]
MIGRATION: NONE [D-RUN-07 not exercised; corrective-migration rule is lint logic]
ONE_MODULE: PASS under D-RUN-21 [no recovery package file changed; repository-level tooling and pipeline only]
NEXT_STEP: Plan gate (orchestrator runs it; not run by this stage).
```
