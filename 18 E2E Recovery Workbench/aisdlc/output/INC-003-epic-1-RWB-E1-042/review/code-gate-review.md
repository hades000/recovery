# Code gate review: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-CODE-001` |
| Gate | Code gate, pre-merge |
| Story | RWB-E1-042 Central configuration service and parameter catalog (EPIC-001, recovery P3/P4) |
| Range | `git diff develop-recovery...feature/RWB-E1-042-parameter-catalog` |
| Tip | `74e4ccb` (2026-11-18 18:26:46 +0700) |
| Inputs read independently | `specify/spec.md` revision 13; `review/spec-gate-review-12.md`; `plan/plan.md` v2 and `plan/tasks.md` v2 (TASK-00..25); `review/plan-gate-review-2.md`; `implement/implementation-report.md`; `implement/unit-tests/report.md`; `implement/review-fix/round2/`; native `backend/build/reports/jacoco/recoveryCoverageReport.xml`; `backend/build/test-results/`; `review/ponytail-review.md`; `review/security-review.md`; `implement/document-gaps.md`; the migration and the 13-row pack CSV |
| Repository | Read only apart from this file. No shared file, build log, spec, plan, code or test was edited. |
| Human sign-off | **Not recorded.** AGENTS.md §9 is unavailable in this run (OPEN-016); no approval is claimed. |

## Status

**FAIL** — 1 High, 2 Low. The High (CODE-001) is a specified behaviour that the current code
contradicts; the two Lows are evidence-record defects. Every other implementation gate passes.

## Findings

| ID | Severity | Finding | Evidence | Remediation |
|---|---|---|---|---|
| CODE-001 | **High** | **An identical repeat of an APPROVED load is refused with 409 instead of returned as `repeat = true`.** `ParameterLoadValidator.validate` runs check 12 (`countApprovedFrom`, `valid_from >= validFrom`) for every row at lines 107-116, before `ParameterLoadHandlerImpl.load` reaches the repeat lookup (`findByContent`, lines 99-104). The first load's own APPROVED rows satisfy `countApprovedFrom`, so a retry of the same file and `validFrom` receives 409 `MSG-P3-027` ("an approved version from ... exists"). SPEC-013 says an identical repeat of a load that is **VALIDATED or APPROVED** returns the existing load with `repeat = true`; §12.5 orders check 11 (repeat) before check 12. The repository's `findByContent` already filters `VALIDATED, APPROVED` (`ParameterValueRepository.java:78-86`), confirming the intended path. | `ParameterLoadHandlerImpl.java:95-104`; `ParameterLoadValidator.java:107-116`; `ParameterValueRepository.java:58-64`; `ParameterConfigIT.java:347-354` (repeat tested only before approval); `ParameterLoadHandlerTest.java:164-175` (validator mocked, so the interaction is not exercised) | Evaluate the identical repeat before check 12 (or move check 12 after the handler's repeat lookup), and add a system test that approves a load and then re-submits the same CSV and date, asserting the same `loadId` with `repeat = true` and no new rows. |
| CODE-002 | Low | The two pre-merge review records are at the **pre-fix** tip `1ffb659`, not `74e4ccb`, and do not contain the verdicts the stage brief cites. `security-review.md` records `verdict: PASS_WITH_LOW_FINDINGS`, 0/0/0/4 (SEC-042-01..04), not `PASS 0/0/0/0`; `ponytail-review.md` ends "Verdict: fix 1 before merge; then 2 and 3." The fixes are present and tested (implementation report), but no re-issued review at the final tip is on disk. | `review/security-review.md` lines 1-10 and 30; `review/ponytail-review.md` final verdict; `implement/implementation-report.md:36-69` | Re-run both reviews at `74e4ccb` (or record that the four SEC findings and the Must/Should items are closed) so the merge evidence carries a final verdict. |
| CODE-003 | Low | The implementation evidence is internally inconsistent. `implementation-report.md:11` says 384 tests and INSTRUCTION 90.8 / BRANCH 81.1; its own Results table (`:75-77`) and the native JaCoCo XML say 386 tests and 90.7 / 80.9 / 95.8. `unit-tests/report.md:9` is the earlier 377-test run (90.3 INSTRUCTION, 81.0 BRANCH, 95.0 METHOD) and is not marked superseded. The `dev.ps1 test` logs (`implement/merge-gate.log` 16:39; `review-fix/merge-gate.log` 17:49) predate `74e4ccb`; only `round2/unit-and-coverage.log` (18:22) and `round2/it-full.log` (18:26) cover the final code. | `implement/implementation-report.md:11`, `:75-77`; `implement/unit-tests/report.md:9`; native `backend/build/reports/jacoco/recoveryCoverageReport.xml`; log timestamps | Correct the status line, version-mark the superseded unit-test report, and re-run `scripts/dev.ps1 test` at the final tip. |

## Gate checklist

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | Spec / AC / TC trace | **PASS** | Spec rev 13; `REQUIREMENT_COVERAGE_RESULT` 57/57, 0 missing, 0 contradictions; AC1-AC11 each mapped to a TC in `plan/tests/scenarios.md:19-29,72-77`; 46 TCs traced. TC-E1-042-12 is **Blocked** with its exit criterion (spec line 1092: RW-PHONECOL identity from RWB-E1-022 and PM-2026.11 from RWB-E1-037) and is not reported as passed. The CODE-001 approved-repeat branch is not covered by TC-16. |
| 2 | Implementation gates: no skipped or weakened test | **PASS (with CODE-001)** | No `@Disabled`, `@Ignore`, `assumeTrue` or assertions disabled in `backend/src/test`; only the standard `@Tag("recovery-it")` / `@Tag("e2e")` tags. Unit 386 tests, 0 failures, 0 skipped; IT 54 tests, 0 failures, 0 skipped. |
| 3 | 80% ×4 native coverage | **PASS** | Native `recoveryCoverageReport.xml`: LINE 2579/2831 = **91.1%**, INSTRUCTION 14041/15476 = **90.7%**, BRANCH 1290/1594 = **80.9%**, METHOD 551/575 = **95.8%**; one BUNDLE rule at 0.80, all production and test-tooling classes in the denominator (4 zero-line classes counted). Frontend `NOT_APPLICABLE`: no `frontend/` change, no OpenAPI change. |
| 4 | No new dependency | **PASS** | `backend/build.gradle.kts` adds only `generateParameterKeys`, the generated `srcDir`, the `compileJava` dependency and `parameterToolingClasses` on both JaCoCo tasks; no dependency declaration added. |
| 5 | No PII / no secret value | **PASS** | Author/approver IDs are UUIDs; fixtures and the migration use the synthetic `00000000-0000-0000-0000-0000000e1042`; no names, account numbers or addresses; no user ID in a log line, event, exception or response; `ace.db.password` is `secret = true` with no value row. |
| 6 | No direct ACE `public` read | **PASS** | No `public.` reference in the new code or migration; the migration uses `${recoverySchema}` only; the P1 consumer fixture reads `access.api.CatalogParameterReader`. |
| 7 | One migration / no merged-migration edit | **PASS** | Only `A backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_042_parameter_catalog_and_seed.sql`; line 1 `-- Story: RWB-E1-042`; no existing migration changed. `V0001` is the next free number; renumber at merge if another migration lands first (D-RCV-28). |
| 8 | Migration seed rows | **PASS** | 19 catalog rows = the 13 pack rows (all 13 `description` texts match the 10 Nov pack CSV character for character) + the 6 D-RCV-36 keys (`temporal.target`, `temporal.namespace`, `temporal.taskqueue.platform`, `temporal.retention.days`, `drools.kiebase.cache.max`, `rules.testcases.min`); 40 approved value rows = 10 TABLE GLOBAL non-secret default keys × 4 environments; self-check block; no secret value. |
| 9 | `@PreAuthorize` on every endpoint | **PASS** | `GET /api/recovery/v1/admin/parameters` carries `@PreAuthorize("@capabilityCheck.require(authentication, 'Rules and parameters', 'R', 'read parameters')")`; refused path returns 403 `MSG-P4-002` with the action text (`ParameterCatalogControllerTest#refusalCarriesTheActionText`, `ParameterConfigIT#readWithoutTheRightIsRefused`). |
| 10 | Flag-off contract | **PASS** | `ParameterCatalogController` and `ParameterLoadHandlerImpl` are `@ConditionalOnProperty(prefix = "rwb.p3", name = "configservice", havingValue = "true")`; `ParameterServiceImpl` and `CatalogParameterReaderImpl` stay registered and serve defaults/ENV; FlagOff context has 3 tests (404, defaults, no handler). |
| 11 | `DG-E042-*` gaps | **PASS** | `DG-E042-ENV-422` and `DG-E042-ROLLBACK-EVENT` are recorded with Blocker = **No**, the two sources, the rationale and an owner; the three IM rows are also recorded. No blocking gap. |
| 12 | Plan file list and shared-file scope | **PASS (notes)** | Every diff path is in `plan.md` "File scope (complete list)" except the two plan-listed entities not created (`DEV-01`, required by SPEC-005) and `ModuleMapLoaderTest.java` (`DEV-05`, one added map entry); both are recorded. The only shared file edited is `backend/build.gradle.kts`; no `aisdlc/` shared document, increment card or build log was edited, and no `shared-updates.md` row was applied here. |
| 13 | One ACE module (D-RUN-21) | **PASS** | Every new class is under `th.co.scb.ace.demo.recovery`; no `common`, `collection`, `platform`, `rules`, `workflow` or `documents` change; the recovery module map adds `casewf.config.api` to `casewf` published only. |
| 14 | D-RUN-19 / D-RUN-20 boundaries | **PASS** | `CatalogParameterReader` is in P4 `access.api`, implemented package-private in P3 `casewf.config`; `ParameterLoadHandler.TABLE = "PARAMETER"` is the dispatcher branch name; no `PARAMETER` SPI bean and no P1, P2 or P4 → P3 edge; `ModulithTest` and `RecoveryBoundaryTest` pass. |
| 15 | AGENTS.md §9 human sign-off | **NOT RECORDED** | OPEN-016; no named human reviewer approval is available or claimed. |

## Verdict

The story is otherwise complete and well evidenced: the spec and plan gates passed, the migration and
seed match the pack and D-RCV-36, the endpoint and capability seam are guarded, the flag-off contract
is tested, and all four native coverage counters clear 0.80. **CODE-001 blocks the merge**: the
approved-load repeat is a specified idempotency path (SPEC-013) and is currently a 409. The two Lows
do not change the code outcome but should be closed before the merge record is used as evidence.

CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 1] [MEDIUM: 0] [LOW: 2]
