---
title: "Code gate review: RWB-TE-001 Recovery module folder and boundary test"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
stage: "review (code gate)"
reviewer: "Compliance Reviewer"
date: "2026-11-18"
diff: "git -C rwb-wt/RWB-TE-001 diff develop-recovery...feature/RWB-TE-001-module-boundary (230 files, +3665/-170; tip 90550d3)"
status: "FAIL"
---

# Code gate review — RWB-TE-001

## Verdict

**FAIL.** The code and both unit gates are sound: 141 backend tests, `recoveryIntegrationTest` 6/6,
18/18 frontend import tests, 28/28 `npm run check`, 80% ×4 on both surfaces, no new dependency, no
PII, no migration change, no direct ACE public read, and BND-1..BND-5 plus the published surface
pass. One required verification is missing: the e2e regression (SPEC-018, TASK-14) has no execution
evidence (DEV-01), and the API Tester stage records the same smoke as `PENDING` and post-merge
(`api-tests/report.md:77-90`). No Critical or High code defect was found; the single Medium is that
verification gap. The Low findings are scope, evidence and traceability hygiene plus two
test-strength notes; they do not change the runtime result.

Evidence reviewed independently: the three-dot diff at `90550d3`, spec v4, plan v7, tasks v7, the
implementation report, `unit-tests/report.md`, the JaCoCo XML/HTML and frontend coverage-summary/LCOV,
`scope-check.md`, `deviations.md` DEV-01..09, both pre-merge reviews, the API Tester and Functional
Automation Test reports (`api-tests/`, `functional-tests/`), and the actual changed source and test
files. `git diff 3cb6c9d 90550d3` is empty, so the reviewed and rebased tips are content-identical.

## Findings

| ID | Severity | File:line | Maps to | Evidence | Required fix |
|---|---|---|---|---|---|
| CODE-001 | Medium | `implement/deviations.md:5`; `implement/implementation-report.md:9-11`; `api-tests/report.md:77-90` | SPEC-018, TASK-14, T-TE001-11, FTS-01..03 | The e2e half of TASK-14 was not run. There is no `implement/backend/e2e.log` and no `e2eTest` results under `backend/build/test-results` (only `test` and `recoveryIntegrationTest`). The API Tester's `api-tests/report.md` section 3 marks `PlatformE2ETest` **PENDING - not run and not passed** and defers it to post-merge; `functional-tests/` is `NOT_APPLICABLE` because UI is out of scope. `it.log` covers the Testcontainers half 6/6 only. The moved `PlatformInfoController` and `TemporalAdminController` therefore have no HTTP path/security/serialization regression after the package move; `PlatformInfoControllerTest` and `TemporalAdminControllerTest` call the methods directly. DEV-01 gives the reason (worktree port rule, port 8080 closed) but the required test is unexecuted. | From the main checkout at `90550d3`, run `./scripts/dev.ps1 up`, `./scripts/dev.ps1 backend` and `./gradlew e2eTest`; save `implement/backend/e2e.log`; then re-gate. Do not merge on the current evidence. A human may explicitly accept the deferral, but it stays visible and blocking until then. |
| CODE-002 | Low | `frontend/eslint.config.js:19-24` | SPEC-014, SPEC-017, AC6, TASK-18, D-RCV-39; DEV-08 | The new `regex: "^(?!\\.\\./).*\\.\\."` rejects `..` segments hidden behind an allowed prefix. It is a tightening consistent with AC6 and D-RCV-39, covered by three new rejected fixtures; `npm run check` 28/28 and `eslint .` exit 0. It is disclosed in DEV-08, but spec.md line 58, plan.md line 229 and the TASK-18 scope list still say `eslint.config.js` is unchanged, and the implementation report's Scope paragraph repeats that. | Record the approved spec/plan deviation in the merge record or shared update; keep the rule. No code change is required. |
| CODE-003 | Low | `implement/unit-tests/report.md:10-11`; `implement/scope-check.md:17,47-48`; `implement/implementation-report.md:16` | [IEG] Unit Test Evidence; SPEC-020, TASK-18 | The headline tables and scope check still print backend 140 / frontend 25 and "`frontend/eslint.config.js` no diff". Final evidence is 141 backend (`review1-suites.txt`) and 28 frontend (`frontend/review1-check.log`, `review1-vitest.log` 18), and the implementation report's review-fix section records 141/28. The final coverage percentages do match the native XML/LCOV, so only counts/scope text are stale. | Refresh the tables to 141/28 and the eslint change, or label the earlier snapshots as pre-fix. Evidence-only fix; the measured coverage is unchanged. |
| CODE-004 | Low | `backend/src/test/java/th/co/scb/ace/demo/recovery/casewf/rules/RuleFactsTest.java:15`; `backend/src/test/java/th/co/scb/ace/boundaryfixture/mapbad/recovery/casewf/events/CaseEventType.java:1` | SPEC-011, SPEC-024, TASK-05, TASK-12; DEV-05/06 | Two files are outside the plan's named lists: `RuleFactsTest` is a twelfth coverage-test class beyond the eleven named in plan.md "Coverage tests"; `CaseEventType` is an extra `mapbad` fixture. Both are disclosed in DEV-05/06 and are test-only; `RuleFactsTest` 4/4 and the `mapbad` eight expected lines pass. | Add both to the plan's coverage-test/fixture file list or accept DEV-05/06 in the merge record. No production impact. |
| CODE-005 | Low | `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryBoundaryTest.java:46-47,113` | BR6, SPEC-026, TASK-09 | `PUBLISHED_PACKAGES` is a literal set of six package names; BR6 says "published packages come from the map, not the test". The exact type list at lines 121-129 is plan-approved and must stay exact, but the package set itself is not derived from `MAP.modules()`/`@NamedInterface`. The security review records the same advisory at lines 177-180. It fails closed only because the map rule separately checks map/annotation equality. | Derive the package set from the map's published entries (or the discovered `@NamedInterface` packages) and keep the exact per-package type list; or record the plan-approved exception. |
| CODE-006 | Low | `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryBoundaryTest.java:145-147` | SPEC-025, T-TE001-14, TASK-09 | T-TE001-14/SPEC-025 name the `casewf` named interfaces as `api`, `rules`, `timers`, `workflow`. The test bounds every name to that set but requires only `rules`, `timers`, `workflow`; an absent `api` interface would still pass. Plan input R3-1 correctly says not to assert the unnamed base-package interface, but after filtering `isUnnamed()` the four named ones can be asserted. | Assert `api` as well if Modulith reports it, or record why the empty `casewf.api` is excluded. The published-surface type test still covers the types. |
| CODE-007 | Low | `implement/backend/task17-run3.log`; `implement/implementation-report.md:101-104` | SPEC-012(b), T-TE001-13, TASK-17 | The three-run negative control is recorded and Run 3 exits 0, but Run 3 is at the pre-fix tip (140 tests). The final `90550d3` was verified with `./gradlew cleanTest test recoveryCoverageVerification` (141) and `npm run check` (28), not with `./scripts/dev.ps1 test`; the wrapper combines those commands and imports `.env`, so the merge-gate proof is one step short at the final tip. | Run `powershell -NoProfile -File scripts/dev.ps1 test` at `90550d3` and save the exit code/log. Low, because both component commands pass and the wrapper is unchanged. |
| CODE-008 | Low | `specify/spec.md:182`; `plan/tests/scenarios.md:48`; `frontend/src/modules/recovery/__tests__/importBoundary.test.ts:13-25` | SPEC-015, AC6, TASK-15; DEV-08 | SPEC-015 and the plan describe 8 rejected + 7 allowed = 15 fixture imports; the committed test has 11 rejected + 7 allowed = 18 because the review fix added the three `..` bypass forms. `functional-tests/report.md` FAT-OBS-02 records the same drift. The test is stronger than the plan, not weaker, and `npm run check` 28/28 is green. | Update SPEC-015 and the plan's test list to the committed 18 (or record the approved three additions in the merge record). |

## Gate checklist

| Gate | Result | Evidence |
|---|---|---|
| Spec / AC trace | PASS | Spec v4 `Status: SUCCESS`, spec gate review-5 PASS 0/0/0/0; 13/13 rules (AC1–AC7, BR1–BR6) mapped to SPEC, TASK and tests. AC3 and AC6 carry the accepted deviations D-RCV-42 / D-RCV-39. X7 is visibly moved to RWB-E1-022 (D-RCV-52). The AC6 test has 11 rejected forms against the spec's 8; that is a test-list drift, CODE-008, not a missed AC. |
| No skipped or weakened test | PASS | No `@Disabled`, `assumeTrue`, `.skip`, `xit` or `xdescribe` in the changed test trees. The moved tests keep their assertions (DroolsRuleEngine 20, Quartz 8, PlatformSmoke 5; PdpaPayloadCodec 18 → 22 after the review fix). `blobClientOnlyInDocumentsModule` is replaced by the map-driven BND-5 exactly as SPEC-009/SPEC-026 direct; no removed assertion appears in the diff. |
| Backend 80% ×4 with native reports | PASS | 141 passed, 0 failed, 0 skipped. LINE 692/710 = 97.46%, INSTRUCTION 3656/3757 = 97.31%, BRANCH 244/256 = 95.31%, METHOD 187/191 = 97.91%. `recoveryCoverageVerification` exit 0; `backend/coverage/recoveryCoverageReport.xml` and HTML; scope is all recovery main classes plus the test-scope tooling, excluding only test classes and fixtures. No main class excluded. |
| Frontend 80% ×4 with native reports | PASS | `importBoundary.test.ts` 18/18; `npm run check` 28/28; lines 91.66% (33/36), statements 91.89% (34/37), branches 88.09% (37/42), functions 82.35% (14/17); `frontend/coverage-summary.json` and `lcov.info` present. Inherited thresholds in `vite.config.ts` (80 ×4) unchanged; no exclusion added. |
| No new dependency | PASS | `backend/deps-diff.txt` shows no difference on runtime, testCompile and testRuntime classpaths (869/925/1093 lines); `frontend/package.json` and lock file are unchanged. ArchUnit, Modulith, SnakeYAML and Mockito were already on the classpath. |
| No literal business value | PASS | The module map is the reference data for names, packages, client packages and client libraries. No new business threshold, route, role or queue literal is introduced; `0.80` is the spec-mandated coverage gate (SPEC-020), not a business value. Failure texts contain class, package and module names only. |
| No PII | PASS | Fixtures use synthetic names (`Synthetic Person`, `synthetic-user`, `probe-1`, zero-padded UUIDs) and the Azurite test key is a local all-`A` placeholder on `127.0.0.1`, not a credential. No real name, ID, account number, address or e-mail in the diff; the security review's scan is consistent. |
| No direct ACE public read | PASS | `noRecoveryClassNamesAPublicTable` is unchanged and green; the only SQL touched is `PlatformInfoController`'s `information_schema` metadata counts, which is pre-existing. No `public.` table read and no new SQL or repository. |
| No merged-migration edit | PASS | The 230-file diff contains no `.sql` file and nothing under `backend/src/main/resources/db/**`. `RecoveryFlywayConfig` moves package only; its history table, placeholder and clean-disabled settings are unchanged. |
| Module boundaries BND-1..BND-5 | PASS | `BoundaryRules` builds BND-1/2/4/5 from the map; breaking and passing fixture worlds prove each. `ModulithTest` is unchanged for BND-3 and green. Real main-code cross-module edges are exactly `casewf.admin → access.api` and `casewf.rules → integration.flags.api`; no cycle. BND-5's diagnostic `{module}` is the P2 module name per the approved data-model §4 (SPEC-010's phrase "allowed client package" differs; plan gate PLAN-007 held it) with no rule effect. |
| Published surfaces | PASS | All 19 modules have base/api/internal `package-info`; every published package has `@NamedInterface(..., propagate = false)`; the six packages that hold types match SPEC-025 exactly (`casewf.rules`, `casewf.timers`, `casewf.workflow`, `integration.flags.api`, `access.api`, `dochub.api`). No Temporal, Quartz or Drools implementation type is public in a published package; `casewf.workflow.internal` / `casewf.timers.internal` are not published. CODE-005/006 are test-strength notes only. |
| AGENTS.md §3 / §4 | PASS | Recovery-only main code; both controllers keep their method checks (`RW-PLATADM`/`RW-AUDIT`, `RW-PLATADM`, `isAuthenticated`); no new dependency, engine, endpoint, migration or business literal; no disabled test; no PII; no `public` table. The `frontend/eslint.config.js` edit is a recovery-scoped tightening (CODE-002). |
| One-file / shared-file scope | PARTIAL | `backend/build.gradle.kts` is the only planned shared file. `frontend/eslint.config.js` is a second shared file (DEV-08) and `RuleFactsTest` / `mapbad.CaseEventType` are extra test files (DEV-05/06); all are disclosed. No production file outside the plan is touched. See CODE-002 and CODE-004. |
| DEV-01 (e2e half of TASK-14) | FAIL | No e2e execution evidence; the API Tester records the same smoke as `PENDING` and post-merge (`api-tests/report.md:88-89`); see CODE-001. The unblock action is named in DEV-01 and repeated here. |
| DEV-08 (eslint.config.js) | PASS | The change is a tightening consistent with AC6 and was disclosed; three new rejected fixtures cover the bypass and the full lint/build is green. The scope wording is stale (CODE-002/CODE-003). |
| DEV-09 (rebase) | PASS | `git diff 3cb6c9d 90550d3` is empty; the tip carries `AISDLC-Run`, `AISDLC-Stage`, `AISDLC-Plan` and `Claude-Session`. |
| Merge gate T-TE001-13 | PARTIAL | Runs 1/2/3 are recorded with the expected exit codes and quoted lines; Run 3 is pre-fix, so the final tip has not been through `dev.ps1 test` (CODE-007). |
| Plan-named files | PARTIAL | Every production and planned test file is named except the three items in CODE-002/CODE-004; all are disclosed in `deviations.md`. |

## Status

REVIEW_STATUS: FAIL
REVIEW_TYPE: CODE_GATE_REVIEW
RUN_ID: INC-002-epic-1-RWB-TE-001
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 7]
REVIEW_BLOCKING: YES [REASON: CODE-001 — the required e2e regression for SPEC-018/TASK-14 has no execution evidence; the API Tester also records it as post-merge]
NEXT_STEP: Run the e2e regression from the main checkout at 90550d3, save the log, refresh the evidence counts and the spec/plan test lists, then re-run this code gate. The seven Low findings may be carried with human disposition; CODE-001 must be closed or explicitly accepted by a human before merge.
CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 7]
