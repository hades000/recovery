---
title: "RWB-TE-001 BR and story test verification"
description: "Fresh local automated evidence for QA, with explicit MR pipeline limitations."
story: "RWB-TE-001"
jira: "TB0001-1235"
run_id: "INC-002-epic-1-RWB-TE-001"
verified_at: "2026-11-10"
---

## Result and provenance

Local automated verification: PASS. Actual GitLab MR pipeline and merge blocking: NOT RUN.

- ACE branch: `feature/TB0001-1235-recovery-module-boundary`.
- ACE commit: `f144a1aa9b26ef30ff052ca4285850345ad9247c`.
- Source worktree was clean before testing and unchanged afterward.
- Backend: Java 21, Gradle unit tests, ArchUnit and Spring Modulith. No application launch,
  database connection, Docker or customer data was needed.
- Backend completed in 23 seconds; frontend completed in 3.36 seconds.
- Backend: 23 passed, 0 failures, 0 errors, 0 skipped.
- Frontend: 2 passed, 0 failures, 0 errors, 0 skipped.

The story has no business AC. D-RCV-16 uses its business rules and remaining test cases for
acceptance. This report verifies the approved specification with synthetic fixtures; it does not
assert literal execution of the original story's pipeline-level examples.

## Commands

Backend, from `ace-monorepo/backend`, with `JAVA_HOME` selecting Java 21:

```bash
DISABLE_SCB_REPO=1 ./gradlew test \
  --tests 'th.co.scb.ace.demo.recovery.architecture.*' \
  --tests 'th.co.scb.ace.demo.ModulithTest' \
  recoveryCoverageReport recoveryCoverageVerification --rerun-tasks --console=plain
```

Frontend, from `ace-monorepo/frontend`:

```bash
npx --no-install vitest run src/modules/recovery/__tests__/importBoundary.test.ts \
  --coverage --reporter=default --reporter=junit \
  --outputFile.junit="$EVIDENCE/frontend/junit.xml"
```

`EVIDENCE` was the absolute path of this report's directory. Both commands returned exit code 0.
No product or test source was edited, and no dependency was installed.

## BR and story case mapping

Methods below are the names recorded in the saved JUnit XML.
For negative fixtures, PASS means the test observed and asserted the expected violation.
It does not mean forbidden dependencies were accepted or a live CI job was intentionally failed.

| Rule | Story case | Local result | Executed assertions |
|---|---|---|---|
| BR1 / BND-1 | TC-TE-001-01 | PASS | `RecoveryBoundaryRulesTest.rejectsRecoveryDependenciesOnUnpublishedCollectionTypes` checks the thrown violation, BND-1 and dependency name. `allowsDependenciesOnPublishedCollectionTypes` checks the permitted alternative. |
| BR2 / BND-2 | TC-TE-001-02 | PASS | `allowsDependenciesOnPublishedCommonTypes` passes. `rejectsRecoveryDependenciesOnUnpublishedCommonTypes` verifies the forbidden alternative and BND-2 diagnostic. |
| BR3 / BND-3 | TC-TE-001-03 | PASS against approved spec | `RecoveryModulithFixtureTest.rejectsDependenciesOnUnpublishedNestedModuleTypes` rejects an internal dependency; `acceptsDependenciesOnPublishedNestedModuleTypes` accepts a published one; `rejectsCyclesBetweenModulesEvenThroughPublishedPackages` rejects a cycle. Existing `ModulithTest.testVerifyApplicationModuleStructure` passes on actual application modules. |
| BR4 / BND-4 | TC-TE-001-04 | PASS | `rejectsEntitiesAndRepositoriesFromOtherRecoveryModules` rejects foreign entities/repositories; `allowsEntitiesAndRepositoriesFromTheSameRecoveryModule` permits own-module data. Common, collection and unmapped ACE entity/repository diagnostics are also tested. |
| BR5 / BND-5 | TC-TE-001-05 | PASS | `rejectsClientLibraryDependenciesOutsideDeclaredClientPackages` detects `java.net.http.HttpClient`; `allowsClientLibrariesOnlyInEachModuleDeclaredClientPackage` permits integration adapter and agent client packages. Name-boundary/lookalike matching also passes. |
| BR6 / module map | TC-TE-001-07 | PASS against approved spec | `RecoveryModuleMapTest.reportsAllModuleMapAndModulithExposureMismatches` rejects an unmapped `rogue` package and declaration mismatches; `acceptsPackagesThatMatchTheModuleMap` accepts a valid map. Four `ModuleMapLoaderTest` methods verify loading the actual map, valid configuration, invalid fields and missing resources. |
| Frontend dependency boundary | TC-TE-001-06 in Test Cases v5, not a row in story section 16 | PASS against approved spec | Vitest `rejects imports outside the recovery allow-list` asserts 11 restricted-import errors on exact fixture lines. `allows recovery-local and explicitly shared imports` asserts no restricted-import error. |
| Access | TC-TE-001-08 | OUT OF SCOPE / NOT RUN | Access guard, test-only endpoint and MSG-P4-002 move to RWB-E1-022 under D-RCV-36 and SPEC-016. This is not a PASS or a waived failure. |

`RecoveryBoundaryTest.verifiesTheRecoveryModuleMapAndExternalBoundaries` also passes against
current main classes using the actual map. Some rules can have no matching runtime dependencies
in a skeleton module; passing and breaking fixtures provide separate enforcement evidence.

Fixture names differ from the original examples (`CollectionSecret` rather than
`CollectorRepository`, dataengine/integration rather than decision/writer, and `rogue` rather than
`vendorx`). BR3 uses Spring Modulith's own diagnostic, not a literal BND-3 message, as accepted in
SPEC-007 and D-RCV-42. Frontend uses `no-restricted-imports` and the approved allow-list
(SPEC-014/015, D-RCV-39), not the legacy `no-collection-import` name.

## Native test and coverage evidence

| Backend JUnit suite | Passed | Failed | Skipped |
|---|---:|---:|---:|
| ModulithTest | 1 | 0 | 0 |
| ModuleMapLoaderTest | 4 | 0 | 0 |
| RecoveryBoundaryRulesTest | 12 | 0 | 0 |
| RecoveryBoundaryTest | 1 | 0 | 0 |
| RecoveryModuleMapTest | 2 | 0 | 0 |
| RecoveryModulithFixtureTest | 3 | 0 | 0 |
| Total | 23 | 0 | 0 |

Backend JaCoCo verification passed all four unchanged 80% thresholds:

| Metric | Covered / total | Percent |
|---|---:|---:|
| Instructions (statement proxy) | 1488 / 1548 | 96.12% |
| Branches | 151 / 170 | 88.82% |
| Lines | 309 / 321 | 96.26% |
| Methods (function proxy) | 63 / 63 | 100.00% |

Scope is recovery production classes plus the approved test-scope architecture tooling, not
all ACE modules. Frontend reports 100% with 0/0 for every metric because there is no measurable
runtime recovery implementation; this is not evidence of runtime UI coverage.

- [Backend run log](backend/test-run.log)
- [Backend exit code](backend/exit-code.txt)
- [Backend native JUnit results](backend/test-results/)
- [Backend HTML test report](backend/test-report/index.html)
- [Backend JaCoCo XML](backend/recoveryCoverageReport.xml)
- [Frontend run log](frontend/test-run.log)
- [Frontend exit code](frontend/exit-code.txt)
- [Frontend native JUnit results](frontend/junit.xml)
- [Frontend coverage summary](frontend/coverage-summary.json)
- [Frontend LCOV](frontend/lcov.info)

## Limits and QA handoff

- D-RCV-05 requires reuse of existing CI, not a new pipeline stage or CI YAML change.
- A failing fixture is asserted within passing local tests. No MR was opened and no live MR
  pipeline was run or intentionally broken in this verification.
- GitLab project setting "Pipelines must succeed" was not checked.
- This was a focused verification, not a fresh full ACE regression, frontend build or SIT/UAT run.
- No production configuration, source code, Jira status or acceptance criteria was changed.
- Evidence files are local workspace artifacts until separately published. Jira comments contain
  a self-contained summary; they must not present an unpublished GitLab file link as available.

## Requirement sources

- [Story section 7 and section 16](../../../../../requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB%20TE%20001%20Recovery%20module%20folder%20and%20boundary%20test%20v1.md)
- [Full Given/When/Then in Test Cases v5](../../../../../requirement/legacy/09-testing-and-quality/recovery-workbench-test-cases-v5-xlsx.md)
- [Approved specification](../../../specify/spec.md)
- [Approved tasks](../../../plan/tasks.md)
- [D-RCV-05, D-RCV-16, D-RCV-36 and related decisions](../../../../../docs/decisions/INC-001-decisions.md)
