---
title: "Plan gate review round 1: RWB-E1-044 (plan v1)"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
gate: Plan (Compliance Reviewer, plan-gate mode)
round: 1
date: 2026-11-18
result: FAIL (0 Critical, 0 High, 3 Medium, 5 Low)
reviewer: Compliance Reviewer agent, started by the orchestrator (Claude Code)
---

# Plan gate review round 1: RWB-E1-044

## 1. Scope

Reviewed, all under `aisdlc/output/INC-001-epic-1-RWB-E1-044/plan/`:

- `plan.md` v1, `tasks.md`, `data-model.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `tests/scenarios.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md` and `agent-run-log.md`.

Checked against:

- The gated spec set `../specify/`: `spec.md` v14-7 (`Status: SUCCESS`, `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 28] [MISSING_RULES: 0] [CONTRADICTIONS: 0]`) and `review/spec-gate-review-7.md` (PASS 0/0/0/0).
- Story files v7, `rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md` §1–§19.
- The document set, `aisdlc/.github/rules/planning-execution-gates.md`, `implementation-execution-gates.md`, `pdlc.md`, `AGENTS.md` §7 and §9, and the applicable run decisions D-RUN-07, -08, -09, -17 and -21 in `AI-SDLC-BUILD-LOG.md`.
- RWB-TE-001 plan v7 (`plan.md`, `tasks.md`, `data-model.md`) and its plan gate round 7 (`review/plan-gate-review-7.md`, PASS 0/0/0/0), plus the current `develop-recovery` code paths and the `[TE-001]` post-merge paths.
- `backend/build.gradle.kts`, `backend/src/main/resources/application.yaml`, `infra/postgres/init/10-load-ace-database.sh`, `20-grants.sql.inc`, `00-roles-and-databases.sh`, `backend/src/main/resources/db/modulemigration/recovery/README.md`, `RecoveryDatabaseIT.java` and `INC-002-epic-1-RWB-TE-001/implement/backend/check-dryrun-baseline.txt`.

No git command, build or container was run. Only this file was written. No question was put to the user (L-RCV-03). The plan gate is the orchestrator's; this review is not the AGENTS.md §9 "Plan approved" sign-off, which stays with the tech lead. No human approval is claimed (OPEN-016; OPEN-050 remains pending).

## 2. Gate checks

| Check | Result | Evidence |
|---|---|---|
| Upstream spec readiness | PASS | Spec `SUCCESS`; spec gate round 7 PASS; coverage 28/28; no `OPEN` CLAR row; 9 shared open items are non-blocking candidates |
| Every in-scope SPEC has a task | PASS | `plan.md` "SPEC to task map": SPEC-001..017 all mapped; 28/28 requirement rows; no orphan |
| Every AC has a test ID | PASS | `tests/scenarios.md` §1: AC1..AC9 all mapped; T-044-01..-22; no AC without a test |
| Exact file paths | PASS | Every path is a `develop-recovery` path or a `[TE-001]` post-merge path; no invented path; `[TE-001]` marked in `plan.md`/`tasks.md`/contract |
| Coverage gate | PASS | One `BUNDLE` rule, LINE, INSTRUCTION, BRANCH and METHOD at 0.80; this story's tooling added to both JaCoCo tasks; no waiver, exclusion or lowered threshold |
| One module (D-RUN-21) | PASS | Recovery only; no `common`/`collection`; `plan.md` "One-module check" cites D-RUN-21; OPEN-050 for ratification |
| No production migration (D-RUN-07) | PASS | None; no `<seq>` fixed; `V<seq>` placeholder only; fixture numbers are test-scope |
| Later-story work is a seam (D-RUN-08) | PASS | SEAM-E044-01..04 named; TE-001 is an upstream dependency, not built here |
| TE-001 v7 base (D-RUN-17) | PASS | `RecoveryFlywayConfig`/`RecoveryMigrationProperties` paths, property split, registration case and coverage include all read from TE-001 plan v7; code gate after TE-001 merge |
| No human approval (OPEN-016) | PASS | `plan.md` line 341; `assumptions.md` line 5; `GATE_REVIEW: PENDING_ORCHESTRATOR`; decisions attributed to the orchestrator (Claude Code) |
| Frontend applicability | PASS | `NOT_APPLICABLE` with scope evidence; no `frontend/` file; `npm run check` in TASK-18 |
| Security, privacy and compliance | PASS | No endpoint/role check; no personal data; synthetic credentials; D-RUN-14 rights only; residual `SET ROLE` recorded as OI-E044-J |
| Test design and fixtures | **FAIL** | PLAN-001..PLAN-003 |
| Document gaps | PASS | DG-L01..L13 carried; PG-E044-01..03 added; all Blocker = No |
| Shared-file discipline | PASS | Only `backend/build.gradle.kts` named; shared updates are proposed, not applied |

## 3. Findings

| ID | Severity | Finding | Evidence | Required fix |
|---|---|---|---|---|
| PLAN-001 | Medium | `MigrationLint.lint(Path)` is planned to scan only `*.sql`, but `t01-nonsql-fail` requires `L-NAME` on `notes.txt`, a non-`.sql` file. `FolderContext` is "the folder's parsed files", so `NameRule` never sees the file. T-044-01 cannot pass as written and ASM-E044-05 is not implemented. | `plan.md` lines 144–145 (`FolderContext` is the parsed files; `MigrationLint` scans `*.sql`); `data-model.md` §3 `t01-nonsql-fail` (line 76); `tasks.md` TASK-03 (line 35) and TASK-04 (line 36, `NameRule` reports a non-`README.md` non-`.sql` file); `spec.md` SPEC-005 and ASM-E044-05 | Make `MigrationLint` list every folder entry, parse `.sql` files, and pass the non-`.sql` names to `NameRule` through `FolderContext` (or give `NameRule` the folder path); include the `notes.txt` case in the complete-list assertion. Do not drop ASM-E044-05. |
| PLAN-002 | Medium | `t01-seqgap-fail` and `t01-seqdup-fail` each hold two non-fix `V` files with the same key `rwb_e1_044`. `L-KEY-DUP` ("at most one non-fix file per key") fires as well, so the complete-list assertions of one `L-SEQ-GAP` and one `L-SEQ-DUP` fail. This also contradicts TASK-03's "each non-fix file has a distinct key" and PA-E044-12. | `data-model.md` §3 lines 79–80 and line 108 (complete list asserted); `tasks.md` TASK-03 line 35; `assumptions.md` PA-E044-12; `spec.md` SPEC-006 | Give the second file in each folder a distinct key and matching line-1 header (for example `rwb_e1_045` / `RWB-E1-045`) so only the sequence rule fires. If the extra finding is intended, add it to the expected list and stop claiming rule isolation (not preferred). |
| PLAN-003 | Medium | `newDatabase(name)` creates a fresh database and only `CREATE SCHEMA recovery`; it does not copy the ACE `public` schema. T-044-17 (d) then counts zero `public` relations (vacuous), and (e)/(f) fail with SQLSTATE 42P01 (undefined table), not 42501. The BR8 database-refusal proof and the T-044-17 green run cannot pass as written. | `plan.md` "Container test design" lines 205–211; `infra/postgres/init/10-load-ace-database.sh` line 21 loads `01-ace-schema-v1.sql` while lines 31–37 create only `recovery`; `spec.md` T-044-17 (d)–(f); `tasks.md` TASK-11 (line 43) and TASK-12 (line 44) | Keep the fresh database but give it the ACE `public` schema and the init roles/grants (for example `CREATE DATABASE <name> TEMPLATE ace`, or load `infra/postgres/schema/01-ace-schema-v1.sql` and `CREATE EXTENSION pgcrypto`), or run T-044-17 against the container's `ace` database. Update TASK-11/-12's red/green expectation. |
| PLAN-004 | Low | TASK-13's verification says `./gradlew check --dry-run` "lists neither coverage task". The baseline lists `:recoveryCoverageReport` as the `test` finalizer; only `recoveryCoverageVerification` is absent. The builder cannot satisfy the wording. | `tasks.md` TASK-13 line 45; `INC-002-epic-1-RWB-TE-001/implement/backend/check-dryrun-baseline.txt` line 8; `backend/build.gradle.kts` line 107 | Reword to "`recoveryCoverageVerification` is absent and `recoveryCoverageReport` remains only as the `test` finalizer; no new `check` dependency". |
| PLAN-005 | Low | TASK-16's verification says a search for `V0` finds none except the pattern text, but the README's line-8 example `V0001__rwb_e1_001_recovery_schema.sql` remains unless reworded; TASK-16 only rewords the "When RWB-E1-001 ships V0001 to V0003" sentence. | `tasks.md` TASK-16 line 48; `backend/src/main/resources/db/modulemigration/recovery/README.md` line 8; `plan.md` line 170 | Include the line-8 example in the reword, or narrow the verification to "no fixed number for RWB-E1-044". |
| PLAN-006 | Low | `tests/scenarios.md` §5 claims empty-folder, missing-folder and unreadable-file coverage, but `data-model.md` §3 has no such fixture and TASK-03 writes only the §3 folders; the T-044-01..-22 list has no test for them. The spec's backend tooling Unit Test Applicability lists "empty folder" and "unreadable ... file" as boundary/error criteria. | `tests/scenarios.md` §5 lines 110–115; `data-model.md` §3; `tasks.md` TASK-03 line 35; `spec.md` Unit Test Applicability backend tooling row | Add `@TempDir`/empty-folder and missing/unreadable-path cases to `RecoveryMigrationLintTest` (or `MigrationLexerTest`) with a test ID, or remove the claim. |
| PLAN-007 | Low | The coverage-type note says the five `OUT_OF_SCOPE_BY_DECISION` rows include "the declined ACE DBA role"; the DBA-role row is `DIRECT_IMPLEMENTATION` (TASK-11/-12). The note names a sixth subject that is not one of the five rows. | `plan.md` line 294 versus line 290 | Remove "and the declined ACE DBA role" from the note, or name the actual fifth row (the pipeline-action row). |
| PLAN-008 | Low | `plan.md` and `agent-run-log.md` say the story was read through §1–§16, but the plan relies on §17 (guardrails) and §19 (out of scope); the read statement understates the evidence. | `plan.md` line 18; `agent-run-log.md` line 23; `plan.md` lines 82 and 328 | State §1–§19, or list the sections read. |

## 4. Coverage table

### SPEC to task and test

| SPEC | Task(s) | Test(s) | Status |
|---|---|---|---|
| SPEC-001 | TASK-08, -10, -14 | T-044-09, -10, -12, -13, -18 | COVERED |
| SPEC-002 | TASK-07, -08 | T-044-08 (1)–(6), -11 | COVERED |
| SPEC-003 | TASK-09, -10 | T-044-09, -12, -14 | COVERED |
| SPEC-004 | TASK-02, -03, -04 | T-044-01..-07, -20..-22 | COVERED |
| SPEC-005 | TASK-03, -04 | T-044-01, -04 | COVERED — fixture defect PLAN-001/PLAN-002 |
| SPEC-006 | TASK-03, -04 | T-044-03 | COVERED — fixture defect PLAN-002 |
| SPEC-007 | TASK-01..-04 | T-044-02, -20, -21, -22 | COVERED |
| SPEC-008 | TASK-03, -04 | T-044-05, -21, -22 | COVERED |
| SPEC-009 | TASK-03, -04 | T-044-20 | COVERED |
| SPEC-010 | TASK-03, -04 | T-044-01..-07; production-folder test | COVERED — boundary/error gap PLAN-006 |
| SPEC-011 | TASK-11, -12, -14, -15 | T-044-10..-18 | COVERED — test setup PLAN-003 |
| SPEC-012 | TASK-05, -06, -14 | T-044-15, -19 | COVERED |
| SPEC-013 | TASK-10, -14 | T-044-13 | COVERED |
| SPEC-014 | TASK-13, -17 | `recoveryCoverageVerification` evidence | COVERED — wording PLAN-004 |
| SPEC-015 | TASK-16 | README and story/plan review | COVERED — wording PLAN-005 |
| SPEC-016 | TASK-02, -04, -19 | T-044-02 seam marker; TASK-19 scope check | COVERED |
| SPEC-017 | TASK-11, -12, -19 | T-044-17; TASK-19 scope check | COVERED — test setup PLAN-003 |

### AC to test

| AC | Test(s) | Task(s) | Status |
|---|---|---|---|
| AC1 | T-044-10 | TASK-14 | COVERED |
| AC2 | T-044-15, T-044-19 | TASK-14, TASK-05 | COVERED |
| AC3 | T-044-11, T-044-08 (5) | TASK-14, TASK-07 | COVERED |
| AC4 | T-044-12, T-044-09 | TASK-14, TASK-09 | COVERED |
| AC5 | T-044-02, T-044-06 | TASK-03 | COVERED — fixture defect PLAN-001 |
| AC6 | T-044-03 | TASK-03 | COVERED — fixture defect PLAN-002 |
| AC7 | T-044-13, T-044-04 | TASK-14, TASK-03 | COVERED |
| AC8 | T-044-14, T-044-09 | TASK-14, TASK-09 | COVERED; job-monitor part out of scope by D-RCV-12, TASK-19 |
| AC9 | T-044-16 | TASK-14 | COVERED |

No SPEC, AC or requirement row is `BLOCKED`; the defects above are the test-design and verification items that block this gate.

## 5. Result

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 3 | PLAN-001, PLAN-002, PLAN-003 |
| Low | 5 | PLAN-004, PLAN-005, PLAN-006, PLAN-007, PLAN-008 |

PLAN-001 to PLAN-003 are the blocking findings. The plan is otherwise strong: every SPEC 001–017 has a task, every AC1–AC9 has a test ID, every file is an exact `develop-recovery` or `[TE-001]` path, the coverage gate is the four-counter 80% `BUNDLE` rule with no waiver, the one-module reading is D-RUN-21, no production migration is planned, later-story work is a seam, and no human approval is claimed.

Under D-RUN-09, the planner remediates all findings and re-gates as `review/plan-gate-review-2.md`. This is the automated plan gate only; the AGENTS.md §9 "Plan approved" sign-off remains with the tech lead, and OPEN-016 and OPEN-050 stay open.

PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 3] [LOW: 5]
