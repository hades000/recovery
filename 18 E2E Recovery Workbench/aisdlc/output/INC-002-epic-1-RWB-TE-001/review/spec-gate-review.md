# Spec gate review: RWB-TE-001 (INC-002-epic-1-RWB-TE-001)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-001-SPEC-005` |
| Stage | Specification gate (fresh gate in this repository, decision D-RUN-05) |
| Artefact | `_v2-baseline/specify/spec.md`, `compliance-validation.md`, `assumptions.md` (written in the 17 v2 workspace for the ACE monorepo) |
| Reviewer | Compliance Reviewer (agent run) |
| Date | 2026-11-17 |
| Baseline | Document set v14: increment card `docs/increments/INC-002-epic-1-RWB-TE-001.md`, story file v7, ADR v3, Decision Log v10, D-RCV-35, D-RCV-36, API Specification v4. Repository: commit `751909e` plus `c22ee73`, `evidence/phase0-standards-audit.md`. |
| Supersedes | Nothing in this repository. `REVIEW-RWB-TE-001-SPEC-004` (PASS, 17 v2 workspace) is history. |

## Status

**`FAIL`**

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | |
| High | 2 | 019, 020 |
| Medium | 4 | 021, 022, 023, 024 |
| Low | 4 | 025, 026, 027, 028 |

Two High and four Medium findings block the handoff to the Implementation Planner. The Technical
Specifier must fix them and the spec gate must run again (pdlc.md, Human Checkpoints).

The spec is still correct on the business rules BR1 to BR6 and on the decided deviations (D-RCV-37 to
D-RCV-43, D-RCV-52). It is wrong about the source in one respect: the v7 story has acceptance
criteria. It is not implementable here as written, because it describes an empty ACE monorepo rather
than this repository's baseline. The baseline already has four technical nested modules, a partial
`RecoveryBoundaryTest`, JaCoCo tasks, the D-RCV-39 ESLint block and Vitest.

## Phase 0 audit items owned by this story

| Audit item | Covered by the spec? | Disposition |
|---|---|---|
| A-01: nothing maps `platform`, `rules`, `workflow` and `documents` to the P1–P10 / S1–S9 design modules | **No.** The spec never mentions the four baseline modules. | Finding 019 (High) |
| A-02: no module map | Yes: SPEC-002, SPEC-003 | Covered |
| A-02: BND-1 and BND-2 missing | Yes: SPEC-005, SPEC-006 | Covered |
| A-02: BND-4 missing | Yes: SPEC-008 | Covered |
| A-02: common and collection stubs missing | Excluded, and the exclusion is legitimate. D-RCV-19 (`allowEmptyShould(true)`), D-RCV-41 map values and OPEN-024 settle it. The fixtures stand in for the packages in test scope (SPEC-011). No main-scope stub is needed. | Legitimately excluded |
| A-02: BND-3 | Yes: SPEC-007, through the existing `ModulithTest` | Covered |
| A-02: BND-6 regex misses unqualified names and the `information_schema` read | The audit gives this hardening to RWB-E1-069. The spec takes BND-6 into this story (SPEC-021) but leaves the baseline test and `PlatformInfoController` without a disposition. | Finding 023 (Medium) |

## Findings

### REVIEW-RWB-TE-001-019: High. The baseline nested modules have no place in the module map (A-01)

- **Evidence:**
  - `backend/src/main/java/th/co/scb/ace/demo/recovery/{platform,rules,workflow,documents}/package-info.java`: four `@ApplicationModule` nested modules with `api` / `internal`. None is one of the 19 names.
  - spec.md SPEC-001 (line 182), SPEC-002 (line 183) and the field matrix (lines 128–129) list only the 19 story §13 names.
  - SPEC-004 (a) (line 185) fails every package under the root that is not a map module. T-TE001-05 (line 262) requires `RecoveryBoundaryTest` to pass on the real main classes. As written, both fail on the baseline.
  - The document set gives homes for most of the baseline code:
    - D-RCV-36 §3.3 publishes `RuleEvaluator` in `recovery.casewf.rules`, `TimerScheduler` in `recovery.casewf.timers` and `WorkflowGateway` in `recovery.casewf.workflow`.
    - Story v7 RWB-E1-071 §13 and BR1: workflow code only in `recovery.casewf.workflow`. RWB-E1-072 §13: `recovery.casewf.rules`.
    - RWB-TE-012 v7 §13: `recovery.dochub.storage`. RWB-E1-044 v7 §13: `recovery.casewf.migration`. RWB-E1-047 v7 §13: `recovery.integration.flags`.
    - API Specification v4: `x-module: P3` for `POST /admin/workflows/smoke` and for the rule-package paths.
  - The baseline instead has `rules.api.RuleEngine`, `platform.api.TimerScheduler`, `platform.api.RecoveryFlags`, `workflow.*` and `documents.*`.
- **Required fix:** Add a SPEC item that gives each baseline nested module and published type a design-module home. There are two options:
  - (a) Relocate the code to the design packages above. Then state the code that moves and the tests that must stay green: `ModulithTest`, the unit tests and `recoveryIntegrationTest`.
  - (b) Map the baseline modules into `recovery-modules.yaml` under their design codes with an explicit transition rule.

  Whichever option is chosen, the published lists in the initial map must match what exists, for example `casewf: [api, rules, timers, workflow]`. The document set does not place the error/Problem handling (`ApiExceptionHandler`, `ProblemFactory`, `ApiError`) or `SecurityConfig` (gap DG-05). Settle their placement by an assumption (L-RCV-03) and an open item for the recovery tech lead. Do not leave it to the planner.

### REVIEW-RWB-TE-001-020: High. The backend coverage gate cannot pass on the stated scope

- **Evidence:**
  - spec.md SPEC-020 (line 201) and the backend Unit Test Applicability row (line 176) measure `th/co/scb/ace/demo/recovery/**`. Both state that main scope "adds only `package-info`, so the measured code is the loader and rule factory".
  - In this repository that scope already holds 28 baseline classes. `backend/build/reports/jacoco/recoveryCoverageReport.xml` (from `test.exec`, 17 Nov 2026 16:56) shows LINE 133/415 (32%) and BRANCH 25/92 (27%). `documents/internal` is at 0/41 lines and `platform/internal` at 24/147.
  - `implementation-execution-gates.md` lines 59 and 62 require the approved production-source scope, untested files included, and turn existing failures into blockers.
  - If finding 019 is settled by relocation, the moved classes are changed by this story and are in scope.
- **Required fix:** Define the approved coverage scope for this story in SPEC-020 and the Unit Test Applicability row. Use either:
  - (a) the story's own production and tooling classes, with the baseline classes listed as excluded and the reason given, or
  - (b) the whole recovery tree with the tests needed to reach 80%.

  State the expected result honestly. If (a) is chosen, record the baseline shortfall as a pre-existing condition with an owner. T-TE001-10 must match the chosen scope.

### REVIEW-RWB-TE-001-021: Medium. The v7 acceptance criteria are unmapped and the spec misstates the source

- **Evidence:**
  - Story file v7 §7 has AC1–AC7 in Gherkin, §5 has X1–X7 and §16 has TC-TE-001-06 (AC6). The text is identical in story files v5, v6 and v7. The increment card lists AC1–AC7.
  - spec.md line 83 says "story §7 has no ACs" and "the story's §5 lists only X7". Line 247 says "The story has no TC-TE-001-06".
  - The Requirement-to-SPEC table (lines 85–103) has no AC rows.
  - AC3 expects the build to fail "with boundary rule BND-3". D-RCV-42 accepts Modulith's text as a deviation from §14 only.
  - AC6 expects rule `no-collection-import` on `src/modules/collection/worklist/WorkList`. D-RCV-39 replaces that rule, but the spec never cites AC6.
  - D-RCV-16 is the premise the spec relies on, and the v7 file contradicts it (gap DG-01).
- **Required fix:**
  - Add AC1–AC7 and X1–X6 to the Requirement-to-SPEC table and the Traceability table.
  - Keep TC-TE-001-06 as the story's frontend test ID instead of saying it does not exist.
  - Record AC3 (Modulith text, D-RCV-42) and AC6 (D-RCV-39 rule name and paths) as accepted deviations against the ACs themselves.
  - Add the AC6 import (`@/modules/collection/worklist/WorkList`) to the T-TE001-07 rejected set.
  - Remove the D-RCV-16 basis, or cite D-RCV-51 as overriding it.

### REVIEW-RWB-TE-001-022: Medium. BND-5 fails on the baseline Blob client

- **Evidence:**
  - `backend/.../recovery/documents/internal/BlobDocumentStore.java` lines 12–20 import `com.azure.storage.blob.*`.
  - spec.md SPEC-002 and SPEC-009 (lines 183 and 190), and the field matrix line 131, set `clientPackages` only for P2 `[adapter]` and P10 `[client]`. `com.azure.storage` is in `clientLibraries` (line 133, D-RCV-41).
  - The spec defers storage to "a later story (for example RWB-TE-012)". The audit (A-04) records that TE-012's Blob store is already baseline.
  - The baseline BND-5 test hard-codes the module, against BR6: `RecoveryBoundaryTest.java` line 75, `documents.internal`.
- **Required fix:** Add the P5 storage client package to the initial map, per RWB-TE-012 v7 §13 `recovery.dochub.storage` or wherever finding 019 places the Blob client. State that the map-driven SPEC-009 replaces the literal baseline test.

### REVIEW-RWB-TE-001-023: Medium. BND-6 (SPEC-021): ownership, map schema and baseline are not reconciled

- **Evidence:**
  - D-RCV-35 §8.2 lists "TE-001 extended so the boundary test allows only `recovery.v_ace_*`" under **RWB-E1-069**.
  - RWB-E1-069 v7 §4 step 5, §10 ("Writes … boundary rule BND-6"), BR8, AC8 and §13 (map gains `sourceViews`) place the rule in E1-069. `backend-context.md` §2 marks BND-6 `DOCUMENTED/REQUIRED (RWB-E1-069)`, and audit A-02 agrees.
  - spec.md SPEC-021 (line 43) takes the rule into this story. It names no map field, but the field matrix (lines 127–133) has none, and SPEC-003 (line 184) fails on an unknown field. SPEC-021 is also missing from the Requirement-to-SPEC, Test scenarios and Traceability tables.
  - Baseline: `RecoveryBoundaryTest.java` lines 33–51 already run a regex BND-6. `PlatformInfoController.java` line 41 queries `information_schema.tables WHERE table_schema = 'public'`.
- **Required fix:** Pick one of two options:
  - (a) Return BND-6 to RWB-E1-069. This story keeps the baseline BND-6 test green and leaves the map schema open for `sourceViews`.
  - (b) Record the decision that brings it forward, then:
    - name the field `sourceViews` in the field matrix, SPEC-003 and `CON-RWB-TE-001-001`, with the 30 names from ACE Source Views v1;
    - map SPEC-021 in all three tables;
    - say whether it replaces the regex test;
    - give the `PlatformInfoController` catalog query a disposition (an allowed exception or a change).

### REVIEW-RWB-TE-001-024: Medium. The change scope describes the ACE monorepo, not this repository's baseline

- **Evidence:**
  - spec.md Change Scope Declaration (lines 75–79) lists `RecoveryBoundaryTest` and the frontend folder as new nodes.
  - SPEC-013 (line 194) expects a folder with one placeholder file. SPEC-015 and SPEC-017 (lines 196 and 198) add Vitest and `@vitest/coverage-v8` and wire an Nx `test` target. SPEC-020 expects a frontend 0/0 coverage result.
  - Baseline:
    - `RecoveryBoundaryTest.java`, including the BS-6.1 Temporal determinism rule (lines 53–70), which the spec does not list as inherited behaviour to preserve;
    - `ModulithTest.java`;
    - JaCoCo tasks (`build.gradle.kts` lines 130–160);
    - the D-RCV-39 ESLint block (`frontend/eslint.config.js` lines 9–42);
    - Vitest 5.1.0 and coverage-v8 (`frontend/package.json`), with coverage on `src/modules/recovery/**` and an 80% threshold (`frontend/vite.config.ts` lines 20–32);
    - runtime recovery frontend code (`api/platform.ts`, `pages/*`), where `evidence/baseline-test.log` shows 91.66% lines;
    - no Nx.
  - RUN-BRIEF says "extend or correct it, never duplicate it".
- **Required fix:**
  - Re-base the Change Scope Declaration, Inherited Existing Behavior, SPEC-013, SPEC-014, SPEC-015, SPEC-017 and SPEC-020 on the baseline:
    - SPEC-013 and SPEC-014 are already met and become inherited behaviour;
    - the frontend work reduces to the AC6 fixture test, the fixture ignore and exclusion, and coverage exclusion of `__fixtures__`;
    - no new frontend dependency;
    - the expected frontend coverage is measured on the existing code.
  - List the existing determinism rule and `ModulithTest` as behaviour that must be kept.
  - Exact file names and commands stay plan inputs (below).

### REVIEW-RWB-TE-001-025: Low. Superseded ADR cited

- **Evidence:** spec.md line 18 and the BR5 row (line 93) cite ADR-005. ADR v3 index line 19 and §ADR-005 say it is superseded by ADR-010 (15 Nov 2026).
- **Required fix:** Cite ADR-010 and REQ-DRI-006 for BR5, and mark ADR-005 as superseded (gap DG-03).

### REVIEW-RWB-TE-001-026: Low. The access-guard row is marked COVERED by a story that does not name it

- **Evidence:**
  - spec.md line 97 marks Flow 5, X7, TC-TE-001-08 and MSG-P4-002 `COVERED` through RWB-E1-022 (D-RCV-52).
  - RWB-E1-022 v7 carries the 403 MSG-P4-002 refusal (X1, AC2). It does not name `RecoveryAccessGuard`, INT-34, the test-only Case record R endpoint or TC-TE-001-08.
  - OPEN-021 aligns only the TE-001 story text.
- **Required fix:** Mark the row as moved out of scope rather than covered, cite RWB-E1-022 v7 X1/AC2 as the destination, and put a `shared-updates.md` row that asks for E1-022 alignment (gap DG-02).

### REVIEW-RWB-TE-001-027: Low. Downstream package names conflict with the module map

- **Evidence:**
  - Story files v7 name top-level recovery packages outside the 19 modules:
    - `recovery.accessadmin.rulepackages` (RWB-E1-072 line 239, RWB-E1-073 line 321), while TE-001 §13 names P4 `access`;
    - `recovery.decisionlog.api` (RWB-E1-014 line 217);
    - `recovery.tools.*` (RWB-E1-065 line 238, RWB-TE-004 line 190);
    - `recovery.generated.*` (RWB-TE-003 line 179).
  - spec.md line 127 handles only `generated`.
- **Required fix:** List these as known conflicts under SPEC-004 and say that the owning story either moves into a map module or extends the map, citing D-RCV-02 (gap DG-04). No code change in this story.

### REVIEW-RWB-TE-001-028: Low. Identifier and count inconsistencies

- **Evidence:**
  - spec.md front matter has `jira: TB0001-1235`, and the card has `EPIC-001` / `RWB-TE-001`.
  - The spec status line cites ACE commit `96b0d1c6` and 17 v2 gate rounds as current.
  - spec.md line 316 has `TOTAL_RULES: 6`, while compliance-validation.md §5 has `TOTAL_RULES: 7`.
- **Required fix:** Align the keys with the card (or record the mapping), mark the ACE evidence as history, and make the rule counts agree.

## Checks performed

| Check | Result |
|---|---|
| Business rules BR1–BR6 against story v7 §8 | PASS: the text is unchanged since the spec was written |
| Acceptance criteria and exceptions against story v7 §5, §7, §16 | FAIL (021) |
| D-RCV-35 / D-RCV-36 alignment | FAIL (019 for the D-RCV-36 §3.3 packages; 023 for BND-6 ownership under D-RCV-35 §8.2) |
| ADR v3 | Low (025). ADR-002 and ADR-010 are applied correctly. |
| Decision Log v10 (DL05, DL07, DL36, DL37) | PASS: DL05 "B from 2 November, then A" matches |
| API Specification v4 | PASS: no endpoint; `NO_API_CHANGE` is correct |
| Implementable against the baseline | FAIL (019, 020, 022, 024) |
| Authorization, PDPA, secrets, personal data | PASS: no runtime authorization, no personal data, no secret |
| Unit-test applicability rows present (both surfaces, 80% on four metrics) | Present; the backend scope is wrong (020) |
| Design evidence | `NOT_REQUIRED`: correct for UI In Scope NO |

## Plan inputs (not spec findings; the plan is re-run for this repository)

1. The application class is `AceRecoveryApplication`, not `DemoApplication`. `ModulithTest` (`backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java`) already runs `verify()` and the Documenter.
2. There are no ACE top-level packages here (`model`, `repository`, `samplemodule`, the 13 `Type.OPEN` package-infos). The BND-4 forbidden patterns stay but match nothing locally.
3. Spring Modulith is 2.1.1, not 2.1.2. ArchUnit 1.5.1 is an explicit `testImplementation` (`build.gradle.kts` lines 31 and 82), so no new dependency is needed. Confirm SnakeYAML with `./gradlew dependencies --configuration testRuntimeClasspath`.
4. The JaCoCo plugin, `recoveryCoverageReport` and `recoveryCoverageVerification` already exist (`build.gradle.kts` lines 130–160). They check LINE and BRANCH only: add INSTRUCTION and METHOD, plus the test-tooling class directory. CI `backend-unit` runs `test recoveryCoverageReport`, not the verification, and `dev.ps1 test` runs only `test`. The plan must say how the verification is run under D-RCV-05 (audit A-09).
5. Extend the existing `th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryTest` (test scope). Keep `workflowImplementationsAreDeterministic`. Replace the literal Blob rule with the map-driven BND-5.
6. `backend/src/test/resources/architecture/` exists and is empty.
7. Frontend:
   - There is no Nx, no `tsconfig.app.json` (only `tsconfig.json`) and no `vitest.config.ts`. Vitest config is in the `vite.config.ts` `test` block.
   - `npm run check` (typecheck, lint, coverage) runs in CI job `frontend-check`.
   - The fixture folder needs an ESLint `ignores` entry, a `tsconfig.json` exclude and a coverage exclude.
   - The fixture test must lint with `ignore: false`.
8. Audit A-11 assigns the import-rule fixture test to RWB-TE-003, but story v7 §13 step 5 and AC6 give it to this story. Build it here and tell TE-003 not to duplicate it (`shared-updates.md`).
9. If finding 019 is settled by relocation, check:
   - Spring component scan under `AceRecoveryApplication`;
   - `@ConfigurationProperties` prefixes;
   - Temporal workflow type names and task queue `rwb-platform`;
   - `RecoveryFlywayConfig` (D-RCV-44: `recoveryIntegrationTest` must run);
   - the frontend is unaffected.
10. Story path `ace-service/src/main/java/<ACE base package>/recovery/` resolves to `backend/src/main/java/th/co/scb/ace/demo/recovery/` (D-RCV-02). `src/modules/recovery/` resolves to `frontend/src/modules/recovery/` (D-RCV-10).
11. The CI file is `.gitlab-ci.yml` with jobs `backend-unit`, `frontend-check` and `backend-recovery-it`. There is no `nx affected`.

## Other observations (for the Context Updater, not findings)

- `backend-context.md` §2 defines BND-1 as "Recovery code stays in the recovery module folder" and marks BND-1 to BND-5 `IMPLEMENTED (RWB-TE-001)`. Story v7 BR1 defines BND-1 as the collection boundary, and in this repository only BND-5 is built (audit A-02).
- `backend-context.md` §1 says "Nx front end". This repository has no Nx.

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 2] [MEDIUM: 4] [LOW: 4]
REQUIREMENT_COVERAGE_RESULT: FAILURE [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 1]  (ACs AC1-AC7 unmapped; finding 021)
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: classification still correct; footprint must be re-based (024)]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
```
