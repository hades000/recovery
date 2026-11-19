---
title: "Functional Automation Test report: RWB-E1-044"
run_id: "INC-001-epic-1-RWB-E1-044"
story: "RWB-E1-044"
stage: "functional-automation-test"
attempt: 1
status: "NOT_APPLICABLE"
prepared: "2026-11-18"
---

# Functional Automation Test report — RWB-E1-044

## Result

`FUNCTIONAL_AUTOMATION_STATUS: NOT_APPLICABLE [RUN_ID: INC-001-epic-1-RWB-E1-044] [COMPONENTS: 0] [CASES: 0]`

No browser suite was created, no Playwright test was executed and no service was started. The story
has no UI workflow in scope: it changes migration lint rules, schema drift comparison and Flyway
startup behaviour only.

## 1. UI Scope Gate — evidence

### 1.1 Approved spec states no UI

`aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/spec.md`, Change Scope Declaration (line 61) and the
adjacent rows (lines 68, 71):

> `| UI In Scope | NO |`
> `| Frontend Changes Required | NO |`
> "This story changes rules and checks only. It adds no route, screen or endpoint."

Same file, `## Frontend Specification` (line 608):

> "N/A. UI In Scope = NO. Story v7 §15 says \"No new screen in this story\". The SCR-44 migration-run
> display is out of scope with no named owner (SPEC-017). `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`."

And line 655: `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]`

Both conditions the UI Scope Gate requires are therefore stated explicitly: `UI In Scope: NO` **and**
`DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`. Line 586 records the frontend unit-test surface as
`NOT_APPLICABLE` with rationale "UI In Scope NO … No file under `frontend/` changes".

### 1.2 Plan and tasks agree — no conflict

They do not disagree with the spec, so the gate rule that requires `BLOCKED` on disagreement does not
apply:

- `plan/plan.md` line 13: `Design Source: NOT_REQUIRED (UI In Scope: NO; DESIGN_EVIDENCE_STATUS: NOT_REQUIRED)`.
- `plan/plan.md` line 33: "no screen task, no `frontend/` file, no `frontend/components.md`".
- `plan/plan.md` line 57: Frontend surface `NOT_APPLICABLE`.
- `plan/plan.md` lines 111-113: "**NOT_APPLICABLE.** UI In Scope NO … No file under `frontend/` is added or changed".
- `plan/plan.md` line 233 (FTS-E044-01): "**NOT_APPLICABLE** - no UI, no screen, no route; the same check is executed as unit tests T-044-01..-07, -20..-22 in `./gradlew test`, which is not a functional automation result".
- `plan/plan.md` line 238: "No functional-automation or API-tester execution is planned: the story adds no screen, route or endpoint. This is recorded as `NOT_APPLICABLE` … not as an executed test."
- `plan/plan.md` line 322: `Screen-to-task mapping` → `NOT_APPLICABLE`.
- `plan/tasks.md` line 22 and line 92: frontend `NOT_APPLICABLE`, effective-screen node groups `NOT_APPLICABLE`.

`plan/frontend/components.md` is correctly absent and is not required on this path (UI Scope Gate
step 3), so no component inventory is claimed or invented.

### 1.3 Independent confirmation from the diff

Worktree `rwb-wt/RWB-E1-044`, branch `feature/RWB-E1-044-db-migrations`; merge base with
`develop-recovery` = `dc2d25b`, HEAD = `89477bc`.

```
git diff --name-status dc2d25b HEAD -- frontend
(empty: no frontend file changed)
```

```
git diff --stat dc2d25b HEAD -- frontend/src/App.tsx frontend/src/modules/recovery frontend/src/api frontend/e2e
(empty)
```

128 files changed in total, and **zero** of them are frontend files. Composition of the diff:

| Area | Files |
|---|---|
| `backend/src/main/java/**` | 4 |
| `backend/src/test/java/**` | 36 |
| `backend/src/test/resources/**` (lint/Flyway fixtures) | 81 |
| `backend/build.gradle.kts`, `.../db/modulemigration/recovery/README.md` | 2 |
| `infra/postgres/init/**` (D-RUN-14 migrator rights) | 2 |
| `docs/stories/RWB-E1-044/**`, `aisdlc/output/**` | 3 |

A filename filter over the diff for `Controller|Page|route|components|*.yaml` returns nothing, which
matches the spec's "no route, screen or endpoint" and `NO_API_CHANGE`.

**No UI surface was missed by the spec**, so a Playwright run would only re-test other stories'
screens. None was run and none is claimed.

## 2. Frontend test suite — recorded, not claimed as functional coverage

The merge gate ran the existing frontend suite (`implement/merge-gate.log`, `npm run check` →
typecheck + ESLint + Vitest coverage, `EXIT_CODE_NPM_CHECK=0`):

```
Test Files  3 passed (3)
     Tests  28 passed (28)
```

This is **Vitest component/unit coverage of unchanged baseline frontend code**, run as a
no-regression check on a story that touches no frontend file. It is not a functional workflow, not a
browser journey, and it is **not** counted as functional automation coverage for RWB-E1-044 in this
report or in `summary.json`.

## 3. Coverage inventory

| Component | Type | Status | Cases |
|---|---|---|---|
| — | — | — | — |

Zero components, zero cases, zero executed, zero passed, zero failed, zero blocked, zero skipped. No
`test-cases.json`, `test_components.py`, `execution.json`, `results/junit.xml`, `logs/`,
`discovery/` or `artifacts/` were produced, because there is nothing to execute.

## 4. Acceptance checks outside UI/API automation

| Acceptance item | Where it lands |
|---|---|
| AC1–AC9 business checks (lint rules, schema drift, MSG-P3-016 failure reporting, D-RUN-14 rights) | Backend JUnit / container `recoveryIntegrationTest` (T-044-01..-22) — not this stage |
| TC-E1-044-08 job-monitor part, TC-E1-044-10 access display | Out of scope by decision (SPEC-017; DG-L10; OI-E044-G) |
| AC8 job-monitor display and SCR-44 | Out of scope, no named owner (SPEC-017) |

Recorded as other-stage / out-of-scope items. This stage does not claim they were executed.

## 5. Findings

None. The spec, plan, tasks and merged diff agree on no-UI scope; no drift was observed.

## 6. Environment

No `APP_URL` was needed or read. No service was started, no browser was launched, no credential read.
No file in the code repository, shared file or build log was modified by this stage.

## 7. Status

```
FUNCTIONAL_AUTOMATION_STATUS: NOT_APPLICABLE [RUN_ID: INC-001-epic-1-RWB-E1-044] [COMPONENTS: 0] [CASES: 0]
COMPONENT_COVERAGE: N/A: UI In Scope = NO
ARTIFACTS: aisdlc/output/INC-001-epic-1-RWB-E1-044/functional-tests/attempt-1/
BLOCKERS: none
```

`NEXT_STEP: Human review of test results and acceptance gaps, then manually start Technical Documenter with RUN_ID=INC-001-epic-1-RWB-E1-044 for the automatic code-review gate and final documentation`
