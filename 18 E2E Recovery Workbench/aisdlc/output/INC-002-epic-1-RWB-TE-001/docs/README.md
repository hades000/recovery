---
title: "RWB-TE-001 Recovery module folder and boundary test — documentation index"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
epic: "EPIC-001"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED — code gate PASS; human review and merge not recorded"
branch: "feature/RWB-TE-001-module-boundary @ 55f1ed4 (base 8675a5c)"
sources: "spec v4, plan v7, tasks v7, implementation and test reports, code gate round 2, security review, ponytail review, plan addendum"
---

# Recovery module boundary (RWB-TE-001)

**DOC ID:** DOC-RWB-TE-001-001 · **Maps to:** SPEC-RWB-TE-001-002, SPEC-RWB-TE-001-004..-010, AC1–AC7, TASK-11

RWB-TE-001 is the build-order 2 technical enabler for EPIC-001 ([S] story file v7, RWB-TE-001 v1;
increment card `INC-002-epic-1-RWB-TE-001`). It gives the recovery module of ACE its **19 design
module folders** and a **build-time boundary test** that refuses a call into another module's
internals and a call to a system of record outside the integration adapters.

The story changes no runtime behaviour. It adds no endpoint, dependency, migration, screen or
configuration key. Two existing controllers move package (with the property-binding split); their
paths, security and responses are unchanged (spec v4, API change assessment).

## 1. The two deliverables

1. **The module skeleton.** `th.co.scb.ace.demo.recovery` now holds 19 nested Spring Modulith
   modules — P1–P10 and S1–S9 from [S] §13 — each with a base `package-info.java`
   (`@ApplicationModule`), an `api` package (`@NamedInterface(name = "api", propagate = false)`) and
   an `internal` package. Published sub-packages carry their own `@NamedInterface`
   (`casewf.rules`, `casewf.timers`, `casewf.workflow`, `integration.flags.api`). The baseline code
   from the four old packages (`platform`, `rules`, `workflow`, `documents`) moved to these homes
   and the old packages are gone.
2. **The boundary toolchain** (test scope only):
   - `recovery-modules.yaml` — the single source of module names, packages, published packages,
     client packages and client libraries (BR6);
   - `ModuleMap` / `ModuleMapLoader` — a validated immutable model of that map;
   - `BoundaryRules` — the map-driven ArchUnit rules BND-1, BND-2, BND-4, BND-5 and the module-map
     rule;
   - fixture worlds under `th.co.scb.ace.boundaryfixture` plus nine fixture maps, one breaking and
     one passing case per rule;
   - `RecoveryBoundaryTest` — runs every rule on the real compiled main classes and the real map;
   - `ModulithTest` unchanged — Spring Modulith `verify()` enforces BND-3 and the no-cycle rule;
   - `importBoundary.test.ts` — proves the inherited D-RCV-39 frontend import rule on 11 rejected and
     7 allowed import forms.

## 2. What a violation looks like

Backend (build log, from the test failure):

```text
Rule BND-1 broken: th.co.scb.ace.demo.recovery.casewf.internal.SampleService depends on
th.co.scb.ace.demo.recovery.collection.internal.CollectorRepository.
Use collection.api or an application event.
```

Unmapped package:

```text
package th.co.scb.ace.demo.recovery.vendorx is not in the module map
```

Frontend (`npm run check`, ESLint `no-restricted-imports`):

```text
D-RCV-39: outside the recovery folder only @/components/ui/**, @/lib/utils, @/utils/* (not cfsc*),
@/contexts/ApiClientContext and @/api/schema are allowed.
```

BND-3 shows Spring Modulith's own `verify()` text rather than a `Rule BND-3 broken:` line — an
accepted deviation, D-RCV-42 (see `COMPLIANCE.md`).

## 3. How a developer runs the checks

**DOC ID:** DOC-RWB-TE-001-002 · **Maps to:** SPEC-012, SPEC-018, SPEC-020, TASK-13, TASK-16, TASK-17

Run from the repository root. Gradle on this workstation needs the JVM temporary-directory property
(RUN-BRIEF "Local stack facts"):

```powershell
$env:JAVA_TOOL_OPTIONS="-Djdk.net.unixdomain.tmpdir=$env:USERPROFILE\.gradle\uds"
```

| Check | Command | Working directory | Notes |
|---|---|---|---|
| Backend unit tests + boundary rules | `./gradlew test` | `backend/` | 22 suites, 141 tests. `ModulithTest`, `RecoveryBoundaryTest`, `RecoveryMigrationLintTest` and the moved tests run here. |
| Backend coverage gate (80% ×4) | `./gradlew test recoveryCoverageVerification` | `backend/` | Note: `./gradlew test` alone does **not** run the verification task, and `dev.ps1 test` does not either. |
| Boundary rules only | `./gradlew test --tests "*RecoveryBoundaryTest"` | `backend/` | 11 tests; fast feedback while editing the map or packages. |
| Integration (Testcontainers, Docker) | `./gradlew recoveryIntegrationTest` | `backend/` | `RecoveryDatabaseIT` 6 tests; required because `RecoveryFlywayConfig` moved (D-RCV-44). |
| API e2e regression | `./scripts/dev.ps1 up` then `./gradlew e2eTest` | repo root, then `backend/` | `PlatformE2ETest` 6 tests against the local stack; proves both relocated controllers answer as before. |
| Frontend check (typecheck, lint, coverage) | `npm run check` | `frontend/` | 28 tests; 80% thresholds on four metrics for `src/modules/recovery/**`. |
| Frontend production build | `npm run build` | `frontend/` | Exit 0. |
| Frontend import test only | `npx vitest run src/modules/recovery/__tests__/importBoundary.test.ts` | `frontend/` | 18 cases (11 rejected, 7 allowed). |
| Local merge gate | `./scripts/dev.ps1 test` | repo root | Runs `gradlew test` and `npm run check`; throws on a non-zero exit. The orchestrator merges only on exit 0 (SPEC-RWB-TE-001-012 (b)). |

The CI jobs are unchanged (D-RCV-05): `backend-unit` runs
`./gradlew test recoveryCoverageReport`, `frontend-check` runs `npm ci`, `npm run check` and
`npm run build`, and `backend-recovery-it` runs the Testcontainers suite. The **verification** task
is not wired into CI in this story; that is audit item A-09, owned by RWB-TE-003 / RWB-TE-011
(SU-10).

## 4. Files that carry the boundary

**DOC ID:** DOC-RWB-TE-001-003 · **Maps to:** SPEC-001..-003, SPEC-011, SPEC-015, SPEC-020,
SPEC-026, TASK-01..-12, TASK-15

| File or folder | Role |
|---|---|
| `backend/src/test/resources/architecture/recovery-modules.yaml` | The module map: 19 modules, two external roots, 16 client libraries. Test resource, not packaged in the jar. |
| `…/recovery/architecture/boundary/ModuleMap.java`, `ModuleMapLoader.java` | Immutable model and SnakeYAML loader; fails with `{file}: {fieldPath}: {problem}`. |
| `…/recovery/architecture/boundary/BoundaryRules.java` | Rule factory; the only place that builds BND-1/2/4/5 and the module-map rule. |
| `…/recovery/architecture/RecoveryBoundaryTest.java` | Applies those rules to real main classes, asserts the package skeleton, the exact published surface and the two inherited checks (BND-6 regex, workflow determinism). |
| `backend/src/test/java/th/co/scb/ace/boundaryfixture/**` | Fixture worlds `passing`, `bnd1`, `bnd2`, `bnd4`, `bnd5`, `vendorx`, `mapbad`, `bnd3fail`, `bnd3pass`, `bnd3cycle`. Test scope only; never packaged with main code. |
| `backend/src/test/resources/architecture/fixtures/*.yaml` | Nine fixture maps, including `bnd5-nop2.yaml`. |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/**/package-info.java` | 61 files: 19 × (module, `api`, `internal`) plus the four extra published packages. |
| `backend/build.gradle.kts` (the two JaCoCo tasks) | Four coverage counters at 0.80 and the test-scope tooling class directory. |
| `frontend/src/modules/recovery/__tests__/importBoundary.test.ts` | The AC6 proof; in-memory sources, real `eslint.config.js` through the ESLint Node API. |
| `frontend/eslint.config.js` | The inherited D-RCV-39 `no-restricted-imports` block, tightened with one `..` rejection (SEC-TE001-01; DEV-08). |

## 5. Current status and gate results

**DOC ID:** DOC-RWB-TE-001-004 · **Maps to:** TASK-13, TASK-14, TASK-16, TASK-17, TASK-18

| Gate or check | Result | Evidence |
|---|---|---|
| Spec gate, round 5 | **PASS** 0/0/0/0 | `../review/spec-gate-review-5.md`; spec v4 `Status: SUCCESS` |
| Plan gate, round 7 | **PASS** 0/0/0/0 | `../review/plan-gate-review-7.md`; plan/tasks v7 |
| Code gate, round 2 | **PASS** 0/0/0/0; 8/8 round-1 findings closed | `../review/code-gate-review-2.md` |
| Backend unit | 141 tests, 0 failures, 0 errors, 0 skipped (22 suites) | `../implement/unit-tests/report.md`, `../implement/backend/review1-suites.txt` |
| Backend coverage, four counters | LINE 97.46%, INSTRUCTION 97.31%, BRANCH 95.31%, METHOD 97.91% (each ≥ 0.80) | `../implement/backend/coverage/recoveryCoverageReport.xml` |
| Integration | `RecoveryDatabaseIT` 6/6, exit 0 | `../implement/backend/it.log` |
| API e2e regression | `PlatformE2ETest` 6/6, exit 0, `BUILD SUCCESSFUL in 52s` | `../implement/backend/e2e.log`; `../api-tests/report.md` §3 |
| Frontend check | 28/28; lines 91.66%, statements 91.89%, branches 88.09%, functions 82.35% | `../implement/frontend/review1-check.log`, `../implement/frontend/coverage-summary.json` |
| Frontend build | exit 0 | `../implement/frontend/review1-build.log` |
| Local merge gate at the final tip | exit 0; backend 141, frontend 28 | `../implement/backend/task17-final-devps-test.log`; `../implement/orchestrator-verify.md` run 6 |
| API tests | `NOT_APPLICABLE` (API In Scope: NO); contract drift: none | `../api-tests/report.md` |
| Functional automation | `NOT_APPLICABLE` (UI In Scope: NO; 0 runtime frontend files changed) | `../functional-tests/report.md` |
| Security review | **PASS**; 1 Medium (SEC-TE001-01) fixed and closed | `../review/security-review.md` |
| Ponytail review | **Ship**; 2 Must + 1 Should + 2 Nice closed | `../review/ponytail-review.md` |

**Documentation snapshot.** The branch is `feature/RWB-TE-001-module-boundary`, tip `55f1ed4`
(230 changed files). The code gate ends at "human review and merge of `55f1ed4`"; **no merge, human
approval, release, SIT or UAT result is recorded in this run**. No new dependency, no migration, no
endpoint change, no UI change.

## 6. Evidence map

| What | Where |
|---|---|
| Story specification (v4) | `../specify/spec.md` |
| Plan and tasks (v7) | `../plan/plan.md`, `../plan/tasks.md` |
| Post-gate change record | `../plan/plan-addendum.md` (A-1..A-4) |
| Implementation report and deviations | `../implement/implementation-report.md`, `../implement/deviations.md` |
| Unit, API, functional evidence | `../implement/unit-tests/report.md`, `../api-tests/report.md`, `../functional-tests/report.md` |
| Scope and guardrail check | `../implement/scope-check.md` |
| Reviews | `../review/` (`spec-gate-review-5.md`, `plan-gate-review-7.md`, `code-gate-review-2.md`, `security-review.md`, `ponytail-review.md`) |
| Coverage reports | `../implement/backend/coverage/`, `../implement/frontend/coverage-summary.json`, `../implement/frontend/lcov.info` |

## 7. Documents in this folder

| Document | Purpose |
|---|---|
| `README.md` (this file) | What the module boundary is, how to run the checks, files, status and gates. |
| `ARCHITECTURE.md` | Module map, published surfaces, BND-1..BND-5, the build-time vs runtime boundary, the frontend import rule. |
| `COMPLIANCE.md` | AC/BR trace, 80% evidence, review evidence, accepted deviations, open items. |

No `OPERATIONS.md` is published: the story adds no runtime component, endpoint, job, migration,
queue, role, feature flag or configuration key, and its only operational procedure is the developer
and merge-gate command set in §3 above. There is nothing to operate, monitor or roll back beyond
reverting the merge request.

### Document ID index

| DOC ID | Where | Maps to |
|---|---|---|
| DOC-RWB-TE-001-001 | README §1–§2 | SPEC-002, SPEC-004..-010; AC1–AC7; TASK-11 |
| DOC-RWB-TE-001-002 | README §3 | SPEC-012, SPEC-018, SPEC-020; TASK-13, TASK-16, TASK-17 |
| DOC-RWB-TE-001-003 | README §4 | SPEC-001..-003, SPEC-011, SPEC-015, SPEC-020, SPEC-026; TASK-01..-12, TASK-15 |
| DOC-RWB-TE-001-004 | README §5 | TASK-13, TASK-14, TASK-16, TASK-17, TASK-18 |
| DOC-RWB-TE-001-005 | ARCHITECTURE §2 | SPEC-002, SPEC-025; TASK-02; CODE-RWB-TE-001-002 |
| DOC-RWB-TE-001-006 | ARCHITECTURE §3 | SPEC-001, SPEC-022, SPEC-025; AC3; TASK-11; CODE-RWB-TE-001-010, CODE-RWB-TE-001-011 |
| DOC-RWB-TE-001-007 | ARCHITECTURE §4 | SPEC-004..-010; AC1–AC5, AC7; TASK-06, TASK-07 |
| DOC-RWB-TE-001-008 | ARCHITECTURE §5 | SPEC-007; AC3; TASK-08 |
| DOC-RWB-TE-001-009 | ARCHITECTURE §6 | SPEC-012, SPEC-018; TASK-13, TASK-17 |
| DOC-RWB-TE-001-010 | ARCHITECTURE §7 | SPEC-013..-015; AC6; TASK-15; CODE-RWB-TE-001-016 |
| DOC-RWB-TE-001-011 | COMPLIANCE §2 | AC1–AC7, BR1–BR6; TASK-03..-09, TASK-11, TASK-15, TASK-16 |
| DOC-RWB-TE-001-012 | COMPLIANCE §3 | SPEC-020, SPEC-024; TASK-01, TASK-12, TASK-16 |
| DOC-RWB-TE-001-013 | COMPLIANCE §4 | SPEC-019; AC6; TASK-18 |
| DOC-RWB-TE-001-014 | COMPLIANCE §5 | SPEC-007, SPEC-014; AC3, AC6 |
| DOC-RWB-TE-001-015 | COMPLIANCE §6 | SPEC-012 (c); TASK-18 |

## 8. Changing the boundary

The map is reference data, not a suggestion. A change to names, packages, published packages, client
packages or client libraries is a normal merge request against `recovery-modules.yaml` **plus** the
matching `package-info.java` annotations, and later code-owner approval once RWB-TE-002 is in place
(D-RCV-21). A later story that adds a published type must, in the same merge request, update the map
and the exact expected list in `RecoveryBoundaryTest.publishedSurfaceIsExactlyTheSpecifiedTypes`;
that test fails by design until it is updated (SU-P02). Never widen the rule to make a red build
green — route the call through the target's `api` or an application event.
