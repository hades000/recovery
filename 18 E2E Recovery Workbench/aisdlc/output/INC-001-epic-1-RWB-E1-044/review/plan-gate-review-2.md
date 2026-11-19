---
title: "Plan gate review round 2: RWB-E1-044 (plan v2)"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
gate: Plan (Compliance Reviewer, plan-gate mode)
round: 2
date: 2026-11-18
result: PASS (0 Critical, 0 High, 0 Medium, 0 Low)
reviewer: Compliance Reviewer agent, started by the orchestrator (Claude Code)
---

# Plan gate review round 2: RWB-E1-044

## 1. Scope

Re-gated, all under `aisdlc/output/INC-001-epic-1-RWB-E1-044/plan/`: `plan.md` v2, `tasks.md` v2, `data-model.md` v2, `tests/scenarios.md` v2, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `agent-run-log.md`, `contracts/backend-apis.json` v2 and `contracts/frontend-integrations.json` v2. Every changed file was re-read in full, not only `agent-run-log.md` "Run 2".

Checked against: `../review/plan-gate-review.md` (round 1, FAIL 0C/0H/3M/5L; PLAN-001..PLAN-008); `../specify/spec.md` v14-7 (`SUCCESS`, 28/28, no `OPEN` CLAR row) and `../review/spec-gate-review-7.md` (PASS 0/0/0/0); story files v7 §1–§19; `planning-execution-gates.md`, `pdlc.md`, `AGENTS.md` §7 and §9; decisions D-RUN-07, -08, -09, -14, -17 and -21 in `AI-SDLC-BUILD-LOG.md`; RWB-TE-001 plan v7 and its plan gate round 7 (`PLAN_GATE: PASS 0/0/0/0`); `backend/build.gradle.kts`, `infra/postgres/init/10-load-ace-database.sh`, `20-grants.sql.inc`, `00-roles-and-databases.sh`, `infra/postgres/schema/01-ace-schema-v1.sql`, `backend/src/main/resources/db/modulemigration/recovery/README.md`, `RecoveryMigrationLintTest.java`, `RecoveryDatabaseIT.java` and `INC-002-epic-1-RWB-TE-001/implement/backend/check-dryrun-baseline.txt`.

No git command, build or container was run. Only this file was written. No question was put to the user (L-RCV-03). The plan gate is the orchestrator's; this is not the AGENTS.md §9 "Plan approved" sign-off, which stays with the tech lead. No human approval is claimed (OPEN-016; OPEN-050 pending).

## 2. Round 1 findings: verification

| ID | Round 1 subject | Current evidence | Verdict |
|---|---|---|---|
| PLAN-001 | Lint scanned only `*.sql`, so `notes.txt` never reached `L-NAME` | `plan.md` lines 144–145 and 182: `FolderContext` holds `parsedFiles` and `otherEntries`; `MigrationLint.lint(Path)` lists **every** entry, parses `.sql`, passes every other name to `FolderContext`, and calls each rule's `checkFolder`; `NameRule` reports every name except `README.md`. `data-model.md` §1 line 21, §3 lines 79 and 111; `tasks.md` TASK-03 (line 35) asserts "exactly one `L-NAME` :0 on `notes.txt` (ASM-E044-05)" and TASK-04 (line 36) states the override; `tests/scenarios.md` T-044-01 (line 32) and §5 (line 114); assumption PA-E044-15. ASM-E044-05 is kept (`assumptions.md` line 5 carries ASM-E044-01..-19 unchanged; spec assumptions line 15). | CLOSED |
| PLAN-002 | Both sequence fixtures reused key `rwb_e1_044`, adding `L-KEY-DUP` | `data-model.md` §3 lines 72, 82–83: second file of `t01-seqgap-fail` is `V0003__rwb_e1_045_third.sql` and of `t01-seqdup-fail` is `V0001__rwb_e1_045_dup.sql`, each with line 1 `-- Story: RWB-E1-045`; expected lists are exactly `L-SEQ-GAP` (detail names `V0002`) and one `L-SEQ-DUP` naming both files, with "no `L-KEY-DUP`". `V0003__rwb_e1_045_third.sql` matches the SPEC-005 name pattern and derives `RWB-E1-045`, so `L-HEADER` cannot fire either; distinct keys also clear `L-FIX-NO-BASE` (no `-- Fix:` line). `tasks.md` TASK-03 and `tests/scenarios.md` T-044-01 agree; PA-E044-12 updated. | CLOSED |
| PLAN-003 | `newDatabase` created a bare database, so T-044-17 (d)–(f) were vacuous or failed with 42P01 | `plan.md` line 208: `CREATE DATABASE <name> TEMPLATE ace`, with the `ace` template state (`01-ace-schema-v1.sql` 62 tables, `pgcrypto`, `20-grants.sql.inc` grants, empty `recovery` owned by `rwb_migrator`); (d) counts real relations and (e)/(f) reach the privilege check (42501, never 42P01). `data-model.md` §7 line 159; `tasks.md` TASK-11 line 43 (red: (a)/(b) fail, (c)/(d) hold, (e)/(f) record `permission denied for schema public`) and TASK-12 line 44 (green: table-level detail); `tests/scenarios.md` T-044-17 line 48; PA-E044-09 records the clone's PUBLIC CONNECT and an alternative. Re-read against `10-load-ace-database.sh` lines 21 and 31–40 and `20-grants.sql.inc`: the template contains the ACE `public` schema (62 `CREATE TABLE`, no view or sequence in `01-ace-schema-v1.sql`), `pgcrypto`, the grants and an empty `recovery`. | CLOSED |
| PLAN-004 | TASK-13's dry-run wording did not match the baseline | `tasks.md` TASK-13 line 45: "`recoveryCoverageVerification` is absent, `recoveryCoverageReport` remains only as the `test` finalizer (baseline line 8)", unchanged from the baseline file. Re-read `check-dryrun-baseline.txt` (line 8 is `:recoveryCoverageReport SKIPPED`) and `backend/build.gradle.kts` (`test` is `finalizedBy("recoveryCoverageReport")`). | CLOSED |
| PLAN-005 | README line-8 example left a fixed `V0001` | `tasks.md` TASK-16 line 48 now rewords **both** the line-8 example `V0001__rwb_e1_001_recovery_schema.sql` and the "When RWB-E1-001 ships V0001 to V0003" sentence to the `V<seq>` form; `plan.md` line 170 records the same two edits; the verification "a search for `V0` finds none" is now satisfiable. Current README line 8 still holds the example, as expected before TASK-16. | CLOSED |
| PLAN-006 | Empty/unreadable-folder coverage was claimed but not planned | `tasks.md` TASK-03 line 35 plans two `@TempDir` methods: an empty folder gives no finding, and a directory named `V0002__rwb_e1_044_unreadable.sql` makes the lint fail closed with an `UncheckedIOException` naming it. `data-model.md` §3 line 111, `tests/scenarios.md` T-044-01 line 32 and §5 line 114 agree; the unsupported "missing folder" claim is gone. | CLOSED |
| PLAN-007 | Coverage-type note named a sixth subject | `plan.md` line 296 names the five `OUT_OF_SCOPE_BY_DECISION` rows (D-RCV-12 job-monitor/run-read/rerun/SCR-44, D-RCV-05 real-environment drift, pipeline action) and states that the ACE DBA row is **not** one of them: it is `DIRECT_IMPLEMENTATION` in TASK-11/-12. The table has exactly five such rows; the ACE DBA row is `DIRECT_IMPLEMENTATION`. | CLOSED |
| PLAN-008 | Read statement understated the story range | `plan.md` line 18 and `agent-run-log.md` line 23 both state §1–§19, including §17 guardrails and §19 out of scope; story files v7 have sections 1 to 19. | CLOSED |

No round-1 finding is carried forward. No remediation text contradicts the spec or the code read.

## 3. Gate checks

| Check | Result | Evidence |
|---|---|---|
| Upstream spec readiness | PASS | Spec `SUCCESS`; spec gate round 7 PASS; `MISSING_RULES: 0`, `CONTRADICTIONS: 0`; CLAR-001..013 `RESOLVED`; nine shared open items are non-blocking candidates |
| Every in-scope SPEC has a task | PASS | `plan.md` "SPEC to task map": SPEC-001..017 all present; the map is identical to v1 (checked line by line), no orphan |
| Every AC has a test ID | PASS | `tests/scenarios.md` §1: AC1..AC9 all mapped; 9 AC rows and 22 test rows identical to v1; T-044-01..-22 |
| Every BR has a task and test | PASS | BR1..BR8 in `plan.md` "Requirement Logic To Task Coverage" (BR1, BR5 rows 1 and 4; BR2 rows 3 and 5; BR3, BR4, BR6, BR7, BR8), all 29 rows unchanged except the coverage-type note |
| Exact file paths | PASS | Current `develop-recovery` paths or `[TE-001]` post-merge paths; `RecoveryMigrationLintTest.java` exists; no invented path |
| Coverage gate unchanged | PASS | One `BUNDLE` rule, LINE, INSTRUCTION, BRANCH, METHOD at 0.80; this story's tooling added to both JaCoCo tasks; no waiver, exclusion or lowered threshold; the section is identical to v1 |
| One-module check unchanged | PASS | `plan.md` "One-module check (D-RUN-21)" is identical to v1; recovery only; OPEN-050 for ratification |
| No production migration (D-RUN-07) | PASS | None; `V<seq>` placeholder only; fixture numbers are test scope (ASM-E044-14); the guidance README is reworded, not numbered |
| Later-story work is a seam (D-RUN-08) | PASS | SEAM-E044-01..04 named, not built; TE-001 is an upstream dependency (D-RUN-17) |
| TE-001 v7 base (D-RUN-17) | PASS | TE-001 plan v7 and its plan gate round 7 re-read: `recoveryCoverageVerification` and `boundaryToolingClasses` exist; the boundary-only include confirms SPEC-014 case 1; registration and property split match |
| Test design and fixtures | PASS | Lint corpus is internally consistent (complete lists, distinct keys, only the intended rule per case); container fixtures and `TEMPLATE ace` state are consistent with the init scripts; `T-044-17` expectations match D-RUN-14 |
| No human approval (OPEN-016) | PASS | `plan.md` line 343; `assumptions.md` line 5; `GATE_REVIEW: PENDING_ORCHESTRATOR`; decisions attributed to the orchestrator (Claude Code) |
| Frontend applicability | PASS | `NOT_APPLICABLE` with scope evidence; no `frontend/` file; `npm run check` in TASK-18 |
| Security, privacy and compliance | PASS | No endpoint or role check; no personal data; synthetic credentials; D-RUN-14 rights only; residual `SET ROLE` recorded as OI-E044-J |
| Document gaps | PASS | DG-L01..L13 carried; PG-E044-01..03; all Blocker = No; no new gap claimed |
| Shared-file discipline | PASS | Only `backend/build.gradle.kts` named as a shared edit; shared updates proposed, not applied |

## 4. Coverage confirmation (unchanged from round 1)

| SPEC | Tasks | Tests | Status |
|---|---|---|---|
| 001 | TASK-08, -10, -14 | T-044-09, -10, -12, -13, -18 | COVERED |
| 002 | TASK-07, -08 | T-044-08 (1)–(6), -11 | COVERED |
| 003 | TASK-09, -10 | T-044-09, -12, -14 | COVERED |
| 004 | TASK-02, -03, -04 | T-044-01..-07, -20..-22 | COVERED |
| 005 | TASK-03, -04 | T-044-01, -04 | COVERED |
| 006 | TASK-03, -04 | T-044-03 | COVERED |
| 007 | TASK-01..-04 | T-044-02, -20, -21, -22 | COVERED |
| 008 | TASK-03, -04 | T-044-05, -21, -22 | COVERED |
| 009 | TASK-03, -04 | T-044-20 | COVERED |
| 010 | TASK-03, -04 | T-044-01..-07; production-folder test | COVERED |
| 011 | TASK-11, -12, -14, -15 | T-044-10..-18 | COVERED |
| 012 | TASK-05, -06, -14 | T-044-15, -19 | COVERED |
| 013 | TASK-10, -14 | T-044-13 | COVERED |
| 014 | TASK-13, -17 | `recoveryCoverageVerification` evidence | COVERED |
| 015 | TASK-16 | README and story/plan review | COVERED |
| 016 | TASK-02, -04, -19 | T-044-02 seam marker; TASK-19 scope check | COVERED |
| 017 | TASK-11, -12, -19 | T-044-17; TASK-19 scope check | COVERED |

AC1 T-044-10 (TASK-14); AC2 T-044-15, -19; AC3 T-044-11, T-044-08 (5); AC4 T-044-12, T-044-09; AC5 T-044-02, -06 (TASK-03); AC6 T-044-03 (TASK-03); AC7 T-044-13, -04; AC8 T-044-14, -09 (job-monitor part out of scope by D-RCV-12, TASK-19); AC9 T-044-16 (TASK-14). No SPEC, AC or requirement row is `BLOCKED`, and no coverage caveat from round 1 remains.

## 5. Findings

None. No new Critical, High, Medium or Low finding; no new contradiction and no coverage regression was found in the remediated set.

## 6. Result

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 0 | — |
| Low | 0 | — |

Under D-RUN-09 this plan may proceed to the orchestrator's handoff. The AGENTS.md §9 "Plan approved" sign-off remains with the tech lead, and OPEN-016 and OPEN-050 stay open.

PLAN_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
