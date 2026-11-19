# Plan gate response: RWB-TE-012 (run 2)

Run: `INC-007-epic-1-RWB-TE-012`. Stage: Implementation Planner, remediation of plan-gate round 1
(`../review/plan-gate-review.md`: `PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 1] [MEDIUM: 1] [LOW: 1]`).
This file maps each finding to the change made. No spec, code, build-log, shared-file or
document-set file was edited; no gate was run and no reviewer was spawned. The plan files were backed
up as `plan.run1.md`, `tasks.run1.md`, `shared-updates.run1.md`, `tests/scenarios.run1.md`,
`agent-run-log.run1.md` and `assumptions.run1.md` before editing.

## 1. Dispositions

| Finding | Severity | Disposition | Change | Where |
|---|---|---|---|---|
| **PLAN-001** | High | Fixed | The six shared configuration files are removed from Builder scope. `shared-updates.md` §0 carries seven exact rows (SH-01 to SH-07) for six files: file, line or section, current value, proposed value, reason and source, consuming task. TASK-08, TASK-16, TASK-18 and TASK-19 verify the orchestrator-applied state and stop with `SHARED_FILE_DEPENDENCY`; TASK-23 checks the Builder diff contains none of the six files. The invalid `[S]` §21 justification is replaced by SPEC-021 (local stack), SPEC-016 (baseline evolution) and the baseline files | `shared-updates.md` §0; `plan.md` "One-module check", "Files added or changed", "Baseline evolution", "Local stack and scripts", scope S-13 and the remediation table; `tasks.md` TASK-08, TASK-16, TASK-18, TASK-19, TASK-23 and "Shared-file dependencies" |
| **PLAN-002** | Medium | Fixed | S-11, the `BlobStorageAdapter` row, the SPEC-018 note and TASK-15/TASK-16 now state that readiness gates `store()` only. `open()` is not gated by readiness (SPEC-015): flag off → NOT_READY; otherwise it does not consult or wait for readiness, attempts the download, and maps TIMEOUT, UNAVAILABLE, ACCESS_REFUSED and BLOB_MISSING through SPEC-013; a TIMEOUT, transport UNAVAILABLE or `ContainerNotFound` outcome may request one background probe and never changes readiness. SPEC-018 defines no `open()`-while-NOT_READY case for T-TE012-07 or T-TE012-18, so no case is added; the plan does not invent behaviour | `plan.md` S-11, adapter row, the "Readiness and `open()`" note, TASK-15/TASK-16; `tests/scenarios.md` T-TE012-07 |
| **PLAN-003** | Low | Fixed | (a) both `[S]` §21 cites are gone; the sources are SPEC-021/016 and the baseline. (b) `tests/scenarios.md` §4 now matches TASK-03's four deterministic stage-1 runs (BE-10, BE-11, BE-12 refusals and the BE-13 accept) and records BE-09 in TASK-22. (c) TASK-04 checks the six named RUNBOOK headings (Apply, PROD lock, Extend, Later PROD applies, DEV spike, Report handling) | `plan.md`; `tasks.md` TASK-03, TASK-04, TASK-18; `tests/scenarios.md` §4 |

## 2. Shared-updates rows now required

Seven rows for six files, in `shared-updates.md` §0:

| Row | File | Consuming task |
|---|---|---|
| SH-01 | `backend/src/main/resources/application.yaml` — add `rwb.dochub` (11 keys) | TASK-08 |
| SH-02 | `backend/src/main/resources/application.yaml` — remove `rwb.blob` lines 98–102 | TASK-16 |
| SH-03 | `backend/src/main/resources/application-local.yaml` — flag `true`, `emulator: true`, string placeholder | TASK-08 |
| SH-04 | `.env.example` lines 23–24 — rename the two keys, same values | TASK-18 |
| SH-05 | `docker-compose.yml:135` — renamed backend variable | TASK-18 |
| SH-06 | `scripts/dev.ps1` `Initialize-EnvFile` — append-missing-keys loop, exact message | TASK-18 |
| SH-07 | `backend/build.gradle.kts:60` — comment names `DocumentContainersConfig` | TASK-19 |

SH-01 and SH-02 are separate rows because the baseline `rwb.blob` bean must keep starting until
TASK-16 deletes `BlobDocumentStore`; removing it earlier would break that context. `README.md` stays a
Builder edit because SPEC-021 names it one.

## 3. Coverage unchanged

```text
SPEC_TO_TASK: 23 of 23 (SPEC-001 to SPEC-023)
AC_TO_EVIDENCE: 12 of 12 (AC1 to AC12)
BR_TO_EVIDENCE: 7 of 7 (BR1 to BR7)
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 37] [TASK_COVERED_RULES: 37] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
SCOPE_BULLETS: 14 of 14 (S-1 to S-14)
BACKEND_COVERAGE_GATE: 80% x4 (LINE, INSTRUCTION, BRANCH, METHOD) over recovery/**, per-class 80% under recovery/dochub/**, no drop
FRONTEND_APPLICABILITY: NOT_APPLICABLE with evidence (UI In Scope NO; DGAP-20)
MIGRATION: none; no fixed number (D-RUN-07)
DEPENDENCY: none
TEST_IDS: T-TE012-01 to -18 unchanged (no test added or removed)
```

No requirement, acceptance criterion, business rule, test ID or task ID changed. The only task-level
changes are the shared-file scope of TASK-08, TASK-16, TASK-18 and TASK-19, the TASK-23 shared-file
check, and the two evidence corrections in TASK-03 and TASK-04. PA-20 in `assumptions.md` had its
source wording aligned with SPEC-016/021; the assumption itself is unchanged.
