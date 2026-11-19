# Spec gate review, round 2: RWB-TE-001 (INC-002-epic-1-RWB-TE-001)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-001-SPEC-006` |
| Stage | Specification gate, round 2 (re-review after remediation of `REVIEW-RWB-TE-001-SPEC-005`) |
| Artefact | `specify/spec.md` (v3, 17 Nov 2026), `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `compliance-validation.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `gate-response.md`, `agent-run-log.md` |
| Reviewer | Compliance Reviewer (agent run, `.claude/agents/compliance-reviewer.md` adapted by `aisdlc/RUN-BRIEF.md`) |
| Date | 2026-11-17 |
| Baseline | Story files v7 (RWB-TE-001 v1 and the v7 stories it cites), D-RCV-35 §8.2, D-RCV-36 §3.3 (`aisdlc/docs/decisions/`), decision register, ADR v3, `aisdlc/.github/contexts/`, `aisdlc/.github/rules/`, `aisdlc/evidence/phase0-standards-audit.md`, `aisdlc/evidence/baseline-test.log`. Code read in this repository on 17 Nov 2026: `backend/` (main, test, `build.gradle.kts`, `build/reports/jacoco/recoveryCoverageReport.xml`), `frontend/` (`eslint.config.js`, `vite.config.ts`, `tsconfig.json`, `package.json`, `src/modules/recovery/`), `.gitlab-ci.yml`, `scripts/dev.ps1`. |
| Previous round | `review/spec-gate-review.md` (`REVIEW-RWB-TE-001-SPEC-005`, FAIL: High 2, Medium 4, Low 4) |
| MCP | Jira, Confluence, GitLab, Figma: not connected (RUN-BRIEF rule 5). `N/A`; local files used. No git run, no code edited. |

## Status

**`FAIL`** (Low findings only; the handoff is not blocked)

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 4 | 029, 030, 031, 032 |

All ten findings of round 1 are resolved. The four new findings are Low. Under `pdlc.md` (Human
Checkpoints) the status stays `FAIL`, the findings stay visible, and the handoff to the
Implementation Planner may proceed with the warning below. A human must dispose of the four Low
findings. The planner can absorb 030 and 031 without a spec change.

`REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.`

## Earlier findings (round 1)

| Finding | Severity | Status | Evidence in v3 |
|---|---|---|---|
| 019: baseline nested modules have no place in the module map (A-01) | High | **Resolved** | Option (a), relocation. The Relocation table (spec lines 194–216) covers every one of the 27 main source files under `recovery/**` that I listed from `backend/src/main/java`, nested types included. The 8 baseline `package-info` files (4 module, 4 `api`) are removed by SPEC-001 (d). Each home is cited and I checked it against the source: D-RCV-36 §3.3 (`casewf.rules`, `casewf.timers`, `casewf.workflow`), E1-072 v7 §13, E1-028 v7 (`recovery.casewf.timers`), E1-071 v7 §13 (`recovery/casewf/workflow`, endpoint in `recovery/casewf/admin`), E1-044 v7 §13 (`recovery.casewf.migration`), E1-047 v7 §12–§13 (`recovery.integration.flags`, published `.api`), TE-012 v7 §13 (`recovery.dochub.storage`). The initial published lists equal what exists (SPEC-025; contract `initialContent`). The tests that must stay green are named: `ModulithTest`, the moved unit tests, `recoveryIntegrationTest`, `e2eTest` (SPEC-018, T-TE001-06, -11). DG-05 is settled by ASM-01/ASM-02 plus open-item row SU-02. I checked the cross-module dependency claim in SPEC-022 (d) against the imports: after the move, only `DroolsRuleEngine` → `RecoveryFlags` (`casewf.rules` → `integration.flags.api`) and `TemporalAdminController` → `ApiError`/`ApiProblemException` (`casewf.admin` → `access.api`) cross modules. That makes no cycle. The four `RecoveryProperties` readers (SPEC-023) are `PlatformConfig`, `PlatformInfoController`, `RecoveryFlywayConfig` and `SecurityConfig`, which matches the code. One wording defect remains in SPEC-022 (c); it is new finding 030. |
| 020: backend coverage gate cannot pass on the stated scope | High | **Resolved** | Option (b): the whole `th/co/scb/ace/demo/recovery/**` main tree plus the test-scope tooling, four counters at 80%, no main class excluded (SPEC-020, backend Unit Test Applicability row, contract `coverage`). The baseline figures match the report: LINE 133/415, BRANCH 25/92, INSTRUCTION 686/2174, METHOD 41/135 (`recoveryCoverageReport.xml`, bundle counters). The expected result is stated honestly: FAIL at baseline, PASS required after SPEC-024 and before the code gate. T-TE001-10 matches. `implementation-execution-gates.md` (scope including untested files, no added exclusions) is respected. |
| 021: v7 ACs unmapped; source misstated | Medium | **Resolved** | AC1–AC7 rows (spec lines 65–71) match story v7 §7 text. X1–X6 are mapped and TC-TE-001-06 is kept. AC3 (D-RCV-42) and AC6 (D-RCV-39) deviations are recorded against the ACs. `@/modules/collection/worklist/WorkList` and the `../` form are in the rejected set (SPEC-015, frontend contract). D-RCV-16 is dropped and D-RCV-51 cited (line 61; DG-01). |
| 022: BND-5 fails on the baseline Blob client | Medium | **Resolved** | `BlobDocumentStore` moves to `dochub.storage`, and the map gives P5 `clientPackages: [storage]` (field matrix, contract). SPEC-009 and SPEC-026 replace `blobClientOnlyInDocumentsModule`. I checked the code: after the move, no other main class imports a D-RCV-41 library. `ProblemFactory` uses `java.net.URI` and `TemporalConfig` uses `java.net.InetAddress`, and neither matches a listed library under the name-boundary rule. |
| 023: BND-6 ownership, map schema and baseline not reconciled | Medium | **Resolved** | Option (a). SPEC-021 is withdrawn and BND-6 returns to RWB-E1-069 (D-RCV-35 §8.2). `noRecoveryClassNamesAPublicTable` is kept unchanged (SPEC-026). The loader accepts the reserved `sourceViews` key unvalidated (SPEC-003, contract schema). This agrees with the E1-069 run (`INC-010…/specify/assumptions.md` ASM-006: TE-001 "leaves `sourceViews` unchanged"). The regex stays green after the move, because `PlatformInfoController` writes `'public'`, not `public.`. |
| 024: change scope describes the ACE monorepo | Medium | **Resolved** | Change Scope Declaration and Inherited Existing Behavior are re-based on this repository. The inherited items exist as described: `ModulithTest`, the determinism rule, the BND-6 regex, JaCoCo tasks (`build.gradle.kts` lines 130–160), the D-RCV-39 block, Vitest 5.1.0 / coverage-v8 5.1.0 with 80% thresholds and the `__tests__` / `i18n` exclusions (`vite.config.ts`), and the CI jobs. SPEC-013/-014 are inherited. The frontend change is one test file with no new dependency (ESLint 9.39.5 ships `lib/types`). The frontend baseline figures match `baseline-test.log` lines 58–61. |
| 025: superseded ADR cited | Low | **Resolved** | BR5 row and SPEC-009 cite REQ-DRI-006 and ADR-010; ADR-005 is mentioned only as superseded (DG-03). |
| 026: access-guard row marked COVERED | Low | **Resolved** | X7 row status `MOVED_OUT_OF_SCOPE`, destination E1-022 v7 X1/AC2; SU-05 asks for E1-022 alignment. |
| 027: downstream package names conflict with the map | Low | **Resolved** | SPEC-004 (g) lists the conflicts and the rule (D-RCV-02, L-RCV-14); SU-09 tells the owners. |
| 028: identifier and count inconsistencies | Low | **Resolved** | Front matter and header use `EPIC-001` / `RWB-TE-001`, and `TB0001-1235` is marked as history. ACE commit `96b0d1c6` is history (line 21). `TOTAL_RULES: 13` is the same in `spec.md` and `compliance-validation.md`. |

Round-1 plan inputs 1–11 are carried in `gate-response.md` and dispositioned in the spec. Plan input 7 is replaced by ASM-07 (in-memory fixtures, no config edits), and I accept that change: it needs no shared config edit and still commits the fixture. Round-1 `document-gaps.md` DG-01..DG-05 are carried into the specify stage's `document-gaps.md` under the same IDs, with DG-06..DG-09 added. Each has two citations and none is a blocker. I agree with every disposition.

## New findings

### REVIEW-RWB-TE-001-029: Low. The re-base request (SU-08) misses RWB-E1-042, the next story in build order

- **Affects:** SPEC-022, SPEC-023, ASM-01, ASM-04; `shared-updates.md` SU-08.
- **Evidence:**
  - `aisdlc/output/INC-003-epic-1-RWB-E1-042/specify/spec.md` (build order 3) puts the whole configuration service in the baseline `platform` module.
    - SPEC-RWB-E1-042-026 places published types in `recovery.platform.api` and the implementation in `platform.internal`.
    - The spec extends `RecoveryProperties`, `RecoveryFlags`, `ApiProblemException`, `ProblemFactory` and `ApiExceptionHandler` (its Impacted Existing Nodes, SPEC-021, lines 346–347).
    - §12.1 states: "If RWB-TE-001's map assigns it elsewhere, moving the package is RWB-TE-001's change."
  - Story file v7 RWB-E1-042 v1 §13 names `recovery.casewf.config`, with published `recovery.casewf.config.api`.
  - This spec removes `platform` (SPEC-001 (d)) and splits `RecoveryProperties` (SPEC-023). It moves the error types to `access` (ASM-01). SPEC-022 (g) moves only classes that an *earlier merged* story added. If E1-042 merges after TE-001, its `platform` package fails the module-map rule (AC7), and its `RecoveryProperties` edits fail to compile.
  - SU-08 re-bases INC-007, INC-008, INC-001 and INC-010, but not INC-003. INC-005 RWB-TE-003 also edits `ApiExceptionHandler` / `ProblemFactory` (its spec line 218). It does write "(or its TE-001 location)", but it is not told the new package.
- **Required fix:** Add an SU-08 entry for INC-003 RWB-E1-042. It should say:
  - the code goes to `recovery.casewf.config(.api)` (story v7 §13), not `platform`;
  - `RecoveryProperties` / `RecoveryFlags` are replaced by module records and `integration.flags.api` (SPEC-023, ASM-03);
  - the problem types are in `access.api` / `access.internal` (ASM-01), so extending them is a cross-module change that E1-042 must plan through `access.api`;
  - the premise "moving the package is RWB-TE-001's change" holds only if E1-042 merges first (SPEC-022 (g)).

  Add a one-line entry for INC-005 RWB-TE-003 with the new homes of `ApiExceptionHandler`, `ProblemFactory` and `TemporalAdminController`. No change to the TE-001 design.

### REVIEW-RWB-TE-001-030: Low. SPEC-022 (c) says no implementation is exposed, but the published `casewf.workflow` and `casewf.timers` packages will expose Temporal and Quartz implementation types

- **Affects:** SPEC-001 (c), SPEC-022 (c), SPEC-025; Relocation table rows for `PdpaPayloadCodec`, `PlatformSmokeWorkflow`, `QuartzTimerScheduler`.
- **Evidence:**
  - SPEC-022 (c) says the classes that land in `casewf.rules`, `casewf.timers` and `casewf.workflow` "are package-private today and stay so, so `propagate = true` exposes no implementation".
  - The same spec's Relocation table keeps three types public:
    - `PdpaPayloadCodec` (`public final class … implements PayloadCodec`, `workflow/internal/PdpaPayloadCodec.java` line 26);
    - `PlatformSmokeWorkflow` (`public interface`, with the nested `Impl` and `Activities` implicitly public, line 17);
    - `QuartzTimerScheduler.TimerDueJob` (`public static class`, line 70).
  - All three move into published packages. With `@NamedInterface` (Spring Modulith 2.1.1, `propagate` default `true`, confirmed from `spring-modulith-api-2.1.1.jar`), every public type there becomes part of P3's published interface.
  - D-RCV-36 §3.3 publishes only `WorkflowGateway` from `recovery.casewf.workflow` and says "There are no other new interfaces". Story v7 RWB-E1-071 says the gateway "never exposes a Temporal type to a caller". After this story, any module could import `PdpaPayloadCodec` or the Temporal-annotated `PlatformSmokeWorkflow`, and Modulith `verify()` would not fail.
  - DG-08 records the `RuleEngine` / `TimerScheduler` signature gap. It does not record these extra published workflow and timer types.
- **Required fix:** Correct SPEC-022 (c) so that it names the public types that land in published packages. Then do one of the following:
  - (a) Accept them as an interim exposure until RWB-E1-071 / RWB-E1-028. Add them to DG-08 and to SU-06 / SU-12 so that the owners narrow the published surface.
  - (b) Keep them out of the named interface, for example by declaring the published package with `@NamedInterface(name = "workflow", propagate = false)` and moving the Temporal implementation into a sub-package. Make `PdpaPayloadCodec` package-private: only `TemporalConfig` and its own test use it.

  The planner can carry either option. Neither changes behaviour.

### REVIEW-RWB-TE-001-031: Low. SPEC-022 (f) undercounts the class-name strings in `DroolsRuleEngineTest`

- **Affects:** SPEC-022 (f), T-TE001-06.
- **Evidence:**
  - SPEC-022 (f) says that only package names and "the two Drools workbook `Import` FQCN strings" change in `DroolsRuleEngineTest`.
  - `backend/src/test/java/th/co/scb/ace/demo/recovery/rules/internal/DroolsRuleEngineTest.java` holds three fully qualified names in workbook cells: line 97 `Import` (`…rules.api.RuleInput`, `…rules.api.RuleOutcome`), and line 98 `Variables` (`th.co.scb.ace.demo.recovery.rules.api.RuleOutcome outcome`).
  - If the Builder follows the spec literally and leaves line 98 unchanged, the decision table fails to compile, and the test fails after the move.
- **Required fix:** Say that every fully qualified class-name string in the test workbook (the `Import` and `Variables` rows) changes to `th.co.scb.ace.demo.recovery.casewf.rules.*`. This is a rename only; no expectation changes. It can be fixed in the plan.

### REVIEW-RWB-TE-001-032: Low. Story §13 step 7, "confirm a failing fixture blocks a merge", has no verification step

- **Affects:** Flow 6 / §13 step 7 row (INHERITED_EXISTING_BEHAVIOR), SPEC-012, status-transition matrix row 1.
- **Evidence:**
  - Story v7 RWB-TE-001 §13 step 7: "Add both checks to the pull request pipeline and confirm a failing fixture blocks a merge". "Done when" requires the boundary test in the main pipeline's unit-test report.
  - The spec maps step 7 to inherited CI behaviour. The status-transition matrix says "the merge is blocked by the failing required job". Nothing in the repository shows that a failing job blocks a merge: that is a GitLab project setting, and no GitLab MCP is connected.
  - The fixtures run in expect-failure mode, so they always pass. No test scenario shows a real violation in main code failing `test` or `npm run lint`.
  - `.gitlab-ci.yml` `backend-unit` does publish the JUnit report, so the "Done when" report part is met.
- **Required fix:** Add a scenario or a plan-level evidence step. Introduce a throwaway violation that is not committed: a main class under `recovery.casewf.internal` importing `java.net.http.HttpClient`, and a recovery file importing `@/modules/collection/x`. Record that `./gradlew test` and `npm run lint` fail with the BND-5 and `no-restricted-imports` texts, then revert. Record the GitLab "pipelines must succeed" setting as `N/A` (no GitLab MCP), as a human-verification item for the merge request.

## Checks performed

| Check | Result |
|---|---|
| Required spec sections and status lines (`specification-execution-gates.md`) | PASS. Every required section is present, and both Unit Test Applicability rows are present and consistent with the change scope. |
| Change classification `NEW_STORY`, UI NO, Logic YES, API NO, `NO_API_CHANGE` | PASS. Two controllers move package with unchanged paths, `@PreAuthorize` and bodies. Neither `/platform/info` nor `/admin/temporal/health` is in API v4 (README item 6), and `/admin/workflows/smoke` keeps `x-module: P3`. |
| Business rules BR1–BR6 and AC1–AC7 against story v7 §7–§8 | PASS. AC3 and AC6 are accepted deviations (D-RCV-42, D-RCV-39). `REQUIREMENT_COVERAGE_RESULT` 13/13 agreed. |
| Exceptions X1–X7 against story v7 §5 | PASS. X7 moved out of scope (D-RCV-52). |
| D-RCV-35 / D-RCV-36 alignment | PASS for packages and BND-6 ownership. Low (030) for extra published types in `casewf.workflow` / `casewf.timers`. |
| ADR v3, Decision Log v10, local decisions D-RCV-02/-05/-19/-21/-37..-44/-51/-52, L-RCV-03/-14 | PASS |
| Implementable against this repository | PASS. I checked the relocation table against all main types, the cross-module imports, `@RestControllerAdvice(basePackages = "…recovery")`, the `@ConfigurationProperties` readers, the CI `backend-recovery-it` path rule, JPA on the classpath for the BND-4 fixture (`spring-boot-starter-data-jpa`), ArchUnit 1.5.1 and the `propagate` attribute. Low items: 030, 031. |
| Backend coverage scope and gate (80% LINE/INSTRUCTION/BRANCH/METHOD) | PASS (planned). The baseline FAIL is stated, and the lift is owned by SPEC-024. |
| Frontend coverage scope and gate (80% four metrics) | PASS (inherited config). The new test file is excluded by the existing `__tests__` exclusion. |
| Authorization, authentication | N/A for new code. `SecurityConfig` and the `@PreAuthorize` checks move unchanged, and SPEC-024 adds tests that assert the existing behaviour. |
| Customer/account data protection, PDPA, personal data in fixtures | PASS. Class and package names only, and synthetic data in coverage tests. No person's name or identifier in the spec set. |
| Audit logging, KYC/AML/consent | N/A. Build-time enabler; no sensitive financial action. |
| Secrets and environment configuration | PASS. Property keys and `application*.yaml` are unchanged, and `rwb.flyway.password` keeps its environment-variable source. |
| Frontend integration and error contract | PASS. No integration; build-log texts only; `ApiError` codes unchanged. |
| No-question rule, assumptions, open items | PASS. ASM-01..-08 have a basis and an effect-if-wrong; SU-02 is the open item. |
| Downstream coordination (`shared-updates.md`) | Low (029) |
| Story §13 step 7 / Done when | Low (032) |
| Design evidence | `NOT_REQUIRED`, which is correct for UI In Scope NO |

## Document gaps found in this review

None new. DG-01..DG-09 in `specify/document-gaps.md` are evidenced and correctly dispositioned. The
E1-042 placement conflict in finding 029 is between a run artefact and story file v7 E1-042 §13. The
story file is clear, so this is a coordination item for SU-08, not a document gap.

## Plan inputs (not findings)

1. **Vitest environment.** The frontend test runs ESLint's Node API under the default `jsdom` environment (`vite.config.ts`). Use a `// @vitest-environment node` docblock and a test timeout that covers the first load of `typescript-eslint`.
2. **Fixture assertions.** Fixtures linted with the full config can also raise `@typescript-eslint/no-unused-vars`. Assert on `ruleId === "no-restricted-imports"` for both sets, or write fixtures that use their imports.
3. **TypeScript settings.** `tsconfig.json` has `noUncheckedIndexedAccess` and includes `src`, so the test must guard `results[0]`.
4. **Property records.** `RecoveryProperties` is registered only by `PlatformConfig`'s `@EnableConfigurationProperties`. Each module record from SPEC-023 needs its own registration.
5. **TC-TE-001-03 fixture tree.** The fixture tree must mirror the real nesting: a fixture `recovery` package with `@ApplicationModule`, and nested `integration` and `decision` modules with `@ApplicationModule`. Otherwise Modulith's nested-module rules are not exercised.
6. **Interim published surface.** If finding 030 is settled by option (b), `@NamedInterface(name = …, propagate = false)` is available in Spring Modulith 2.1.1.
7. **One-module rule.** AGENTS.md §7/§9 (a plan "touches one module"): the relocation touches P2, P3, P4 and P5 code. Read "module" as the ACE module (recovery), as AGENTS.md §2–§3 do. The plan should state that reading, because story §13 step 1 itself creates all 19 nested modules.

## Other observations (not findings)

- Story v7 §17 says that breaking fixtures "stay in `src/test`". The frontend fixtures are string constants in `src/modules/recovery/__tests__/` (ASM-07). The intent, that they never ship, is met, and the spec's Guardrails line states the placement.
- `TemporalConfig.SmokeActivities` (activity I/O) lands in `casewf.workflow`. Story v7 E1-071 BR1 puts activities in `recovery.casewf.activities`. E1-071 owns that split (SU-12).

## Status lines

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] [COVERED_RULES: 13] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: build-time rules and package relocation without behaviour change]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
PRIOR_FINDINGS: 019-028 RESOLVED (10 of 10)
```
