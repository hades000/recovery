---
title: "RWB-TE-001 review remediation evidence"
description: "Approved BND-4 diagnostic deviation, regression evidence, and handoff notice trace."
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
date: "2026-11-10"
status: "IMPLEMENTED_AWAITING_REVIEW"
---

## Story-owner approval and specification deviation

Jesniphat Pukkham approved the exact fallback wording as story owner on 2026-11-10 at
14:11:19 +07:00 in [Jira comment 1783131](https://scbjira.atlassian.net/browse/TB0001-1235?focusedCommentId=1783131).
The approval explicitly permits recording this as a deviation from SPEC-RWB-TE-001-010 in
implementation evidence without a specification or plan rerun.

Approved diagnostic for BND-4 targets outside recovery modules and the mapped common/collection
roots:

```text
Rule BND-4 broken: {class} depends on {dependency}. Use the owning module's service or published interface, not its entity or repository.
```

Only the fallback recommendation changes. The diagnostic prefix, dependency predicate, same-module
exception, common/collection recommendations, and BND-1/BND-2/BND-5 behavior remain unchanged.
Entities and repositories are still rejected even if they are in a published package.
The approved specification and plan files were not edited.

## Finding-to-fix trace

| Finding | Requirement and implementation trace | Action and evidence | Disposition |
|---|---|---|---|
| REVIEW-RWB-TE-001-033 | TASK-RWB-TE-001-20; SPEC-RWB-TE-001-016..020; CODE-RWB-TE-001-01..06 | [OPEN-023 notice, comment 1782843](https://scbjira.atlassian.net/browse/TB0001-1235?focusedCommentId=1782843); [RWB-E1-044 planner notice, comment 1782844](https://scbjira.atlassian.net/browse/TB0001-1205?focusedCommentId=1782844) | Both notices posted. Receipt replies are not a plan gate. Finding awaits reviewer verification. |
| REVIEW-RWB-TE-001-034 | SPEC-RWB-TE-001-008/-010; TASK-RWB-TE-001-06..08; CODE-RWB-TE-001-03; TEST-RWB-TE-001-BE-01 | Approval above; test-first regression and native results below | Approved fallback implemented; finding awaits reviewer verification. |

Neither review finding nor the original `FAIL` status was changed. No formal code-gate rerun or
later lifecycle stage was started. Publication and HV-1 remain pending a separate user instruction.

## Changed ACE files

All paths below are relative to the ACE repository. Existing uncommitted changes were preserved.

- `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryBoundaryRules.java`:
  use the approved recommendation when no target module is found.
- `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryBoundaryRulesTest.java`:
  assert complete diagnostics for both unmapped entity and repository dependencies; verify the
  collection recommendation remains unchanged. Existing common and same-module tests remain.
- `backend/src/test/java/th/co/scb/ace/recoveryfixture/bnd4ace/model/AceEntity.java` and
  `backend/src/test/java/th/co/scb/ace/recoveryfixture/bnd4ace/repository/AceRepository.java`:
  synthetic ACE-shaped targets outside the fixture recovery and external roots.
- `backend/src/test/java/th/co/scb/ace/recoveryfixture/bnd4/dataengine/internal/UsesAceData.java`:
  source fixture that depends on both ACE-shaped targets.
- `backend/src/test/java/th/co/scb/ace/recoveryfixture/bnd4/collection/internal/CollectionEntity.java`
  and `backend/src/test/java/th/co/scb/ace/recoveryfixture/bnd4/dataengine/internal/UsesCollectionEntity.java`:
  mapped collection negative fixture.

No main-source, shared build, frontend, dependency, module-map, or migration changes were made by
this remediation. Fixtures remain under the approved test-only root, outside the ACE application
scan. No real ACE entity or repository was imported into a fixture.

## Test-first execution

Commands ran in `ace-monorepo/backend` with `DISABLE_SCB_REPO=1`.

| Step | Gradle arguments | Exit | Duration | Evidence |
|---|---|---:|---|---|
| Red | `test --tests th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryRulesTest --rerun-tasks` | 1, expected | 27s | [Log](./unit-tests/backend/remediation-034/red.log), [JUnit XML](./unit-tests/backend/remediation-034/red.xml) |
| First green attempt | `checkstyleTest test --tests th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryRulesTest` | 1 | 7s | [Log](./unit-tests/backend/remediation-034/green.log); assertions passed, three new assertion lines exceeded 100 characters |
| Green after wrapping assertion lines | Same focused command | 0 | 5s | [Log](./unit-tests/backend/remediation-034/green-rerun.log), [JUnit XML](./unit-tests/backend/remediation-034/green/TEST-th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryRulesTest.xml) |
| Full verification | `checkstyleMain checkstyleTest test recoveryCoverageReport recoveryCoverageVerification --rerun-tasks` | 0 | 1m 55s | [Log](./unit-tests/backend/remediation-034/full-verification.log), [JUnit XML](./unit-tests/backend/remediation-034/test-results/), [JaCoCo XML](./unit-tests/backend/remediation-034/recoveryCoverageReport.xml) |

The red run had 12 tests, 11 passing and 1 failing specifically because the old `common.api`
fallback did not match the approved diagnostic. The focused green run passed all 12.
The full backend suite passed 740 tests with 274 existing excluded end-to-end scenarios skipped,
zero failures, and zero errors. Compilation and Checkstyle passed. The existing Modulith checks
and same-module entity/repository passing fixture remain green.

## Current remediation unit-test evidence

| Surface | Passed | Failed | Skipped | Statements % | Branches % | Functions % | Lines % | Required % | Status | Evidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Backend | 740 | 0 | 274 | 96.12% (1488/1548) | 88.82% (151/170) | 100.00% (63/63) | 96.26% (309/321) | 80% | PASS | [Native reports and logs](./unit-tests/backend/remediation-034/) |
| Frontend | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | NOT_APPLICABLE | No frontend changes in this diagnostic-only remediation; original frontend results remain in [unit-test report](./unit-tests/report.md) |

Coverage uses the unchanged approved recovery scope, including the test-scope module-map loader
and boundary tooling. JaCoCo instructions represent statements and methods represent functions.
No threshold, exclusion, test tag, or task wiring was changed. No database or running application
was needed for the focused regression; the full suite uses its existing test configuration.

## Bounded AI first-pass review

Reviewed only the remediation edits against the pre-remediation implementation read in this run,
the approved story-owner comment, and ACE coding standards. The implementation is uncommitted,
so a `HEAD` comparison would mix the prior story implementation with this remediation.
The `code-review` skill was loaded; its configured `docs/agents/issue-tracker.md` helper remains
absent. No setup or new tooling was added; Jira approval was verified directly.

### Standards

No actionable findings in this remediation. Changes stay in approved test-scope locations and
preserve unrelated work. Checkstyle enforces the line-length convention.

### Spec

No actionable findings in this remediation. Both complete fallback messages match the approved
wording; common, collection, and recovery-module recommendations remain covered by passing tests.
The rejection predicate is unchanged.

Summary: Standards 0 findings; Spec 0 findings. This bounded self-review does not replace
Compliance Reviewer's code-gate decision or resolve the existing findings.

## Next human action

Request a code-gate re-review using the original findings, the two notice links, the story-owner
approval, this deviation record, and the fresh native test/coverage evidence. Do not treat
implementation completion as reviewer disposition. The story implementation was committed and
pushed to ACE as `f144a1aa9b26ef30ff052ca4285850345ad9247c`, and ACE MR !285 was opened. Its
pipeline 220557 is skipped, so HV-1 and reviewer disposition remain pending.
