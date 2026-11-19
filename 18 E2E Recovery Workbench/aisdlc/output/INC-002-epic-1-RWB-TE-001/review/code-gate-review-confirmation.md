# Code gate review (confirmation): RWB-TE-001

> Provenance: the Compliance Reviewer agent returned this review as text. The orchestrator saved it here.
> The wording is condensed slightly; the finding IDs, files, lines and the gate line are unchanged.

| Field | Value |
|---|---|
| Run | `INC-002-epic-1-RWB-TE-001` |
| Story | RWB-TE-001: Recovery module folder and boundary test |
| Reviewed | Merge `dc2d25b` on `develop-recovery` (`git diff dc2d25b^1 dc2d25b`). Files at `27567ed` checked for later changes to the TE-001 tests |
| Reviewer | Compliance Reviewer, code gate mode (Claude Opus 5.5, high effort), read only |
| Why | Most of the build after the first red commit, the pre-merge reviews and code gate rounds 1 and 2 ran in opencode on DeepSeek v4.1 Flash (D-RUN-26). This is an independent Opus 5.5 gate on what was merged |
| Not done | No tests or builds were run. Post-merge `dev.ps1 test`, `it` and `e2e` at `27567ed` are taken as green from the build log |
| Out of scope | REVIEW-001 H3 (coverage verification not in CI) and L10 (literal roles in moved controllers), fixed or registered under REVIEW-001 |
| Rule | D-RUN-09: any finding, Low included, fails the gate |

## 1. Inputs read

- `specify/spec.md` v4 (field-level behaviour matrix, SPEC-RWB-TE-001-001..026, AC1..AC7, BR1..BR6).
- `plan/plan.md` v7 and `plan/plan-addendum.md` A-1..A-4.
- `implement/implementation-report.md`, `implement/deviations.md` (DEV-01..09), `implement/unit-tests/report.md`, and the coverage and test evidence under `implement/`.
- `api-tests/report.md`, `functional-tests/report.md`, `docs/*`.
- `review/code-gate-review.md` (round 1, FAIL 0/0/1/7), `review/code-gate-review-2.md` (round 2, PASS 0/0/0/0), `review/ponytail-review.md`, `review/security-review.md`.
- AGENTS.md §3 and §4; `REVIEW-001-first-four-stories/evidence-audit.md` and `code-quality-review.md`.
- The whole merge diff: the boundary tooling (`BoundaryRules`, `ModuleMapLoader`, `ModuleMap`), `RecoveryBoundaryTest`, `BoundaryRulesTest`, `ModuleMapLoaderTest`, `ModulithFixtureTest`, the fixtures under `th.co.scb.ace.boundaryfixture` and the nine fixture maps, `recovery-modules.yaml`, `build.gradle.kts`, `frontend/eslint.config.js`, `importBoundary.test.ts`, and the main-code move into the 19 design modules.

## 2. Acceptance criteria and boundary rules against tests

| AC / rule | Test that would fail if the behaviour broke | Must-fail fixture asserted | Result |
|---|---|---|---|
| AC1 / BND-1 | `BoundaryRulesTest` bnd1 cases (exactly 2 violation lines); `RecoveryBoundaryTest.bnd1` on main classes | Yes | OK |
| AC2: `common` api dependency passes | `BoundaryRulesTest.commonApiDependencyPassesEveryRule` | Passing fixture | OK |
| BND-2 (including sub-packages) | `BoundaryRulesTest` BND-2 cases, including `SecretHelper` | Yes | OK |
| AC3 / BND-3 | `ModulithFixtureTest` bnd3fail, bnd3pass, bnd3cycle; real classes: `ModulithTest` | Yes | OK |
| AC4 / BND-4 | `BoundaryRulesTest` (exactly 4 lines) | Yes | OK |
| AC5 / BND-5 | `BoundaryRulesTest` (exactly 4 lines) and the nop2 world (6 lines); T-TE001-09 | Yes | OK |
| AC6: frontend import boundary | `importBoundary.test.ts`: 11 rejected (1 message each), 7 allowed (0 messages) | Yes | OK. 18 cases instead of 15 is recorded (A-3, DEV-08) |
| AC7 / BR6: map is the single source | `BoundaryRulesTest` vendorx world; `ModuleMapLoaderTest` (28 tests); `PUBLISHED_PACKAGES` derived from the map | Yes | OK, except CONF-TE001-01 |
| Module-map rule (SPEC-004) | `BoundaryRulesTest` mapbad world (exactly 8 lines); `moduleMapRule`; `everyMapModuleHasApiAndInternalPackageInfo` | Yes | OK |
| SPEC-025: exact published surface | `publishedSurfaceIsExactlyTheSpecifiedTypes`; `casewfNamedInterfacesAreTheSpecifiedBoundedSet` | n/a | Behaviour OK. The documentation overstates it: CONF-TE001-02 |
| SPEC-020 / SPEC-024: coverage | Four JaCoCo limits at 0.80; tooling measured; tests and fixtures excluded; `RuleFactsTest` (A-2) | n/a | OK. CI wiring is REVIEW-001 H3 |

## 3. No weakened or skipped tests

- `blobClientOnlyInDocumentsModule` was replaced by the map-driven BND-5 (SPEC-010), which is stricter.
- The determinism rule moved to `.casewf.workflow..` with a guard test. `noRecoveryClassNamesAPublicTable` is unchanged.
- No `@Disabled`, `assumeTrue` or loosened assertion. Violation counts are exact everywhere.
- E1-042's later changes add `casewf.config.api` to the exact lists; they extend the tests.
- The ESLint change (A-1, DEV-08) only adds a rule.

## 4. AGENTS.md §3 and §4

The main-code diff is package and import moves, plus: `PdpaPayloadCodec` made package-private,
`TemporalProperties` made public, and the properties split into `RecoveryFlagProperties`,
`PlatformInfoProperties`, `RecoveryMigrationProperties` and `RecoverySecurityProperties`, each with its own
prefix and validation. The diff adds no business literal, no personal data, no public table and no migration.
The literal `"P2"` in the BND-5 message text is recorded in plan PA-04 and data-model §4; matching is map-driven.

## 5. Deviations

DEV-01..09, A-1..A-4 and PA-04 each have rationale and evidence, except the false statement in A-4 (CONF-TE001-02).

## 6. Evidence figures

| Claim | File | Match |
|---|---|---|
| Backend 141 tests, 0 failures | `backend/review1-suites.txt` (22 suites) | Yes |
| Coverage: instruction 97.31, branch 95.31, line 97.46, method 97.91 | `backend/coverage/recoveryCoverageReport.xml`, `totals.txt` | Yes |
| Frontend 28 tests; lines 91.66, statements 91.89, branches 88.09, functions 82.35 | `frontend/review1-check.log`, `coverage-summary.json` | Yes |
| Import-boundary test 18/18 | `frontend/review1-vitest.log` | Yes |
| Round 1 FAIL 0/0/1/7, round 2 PASS 0/0/0/0 | `review/code-gate-review.md:75`, `review/code-gate-review-2.md:82` | Yes |
| Merge message test and coverage figures | commit `dc2d25b` | Yes |

## 7. Findings

### CONF-TE001-01 (Low): the loader does not reject a duplicate `published` entry

- **Where:** `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/boundary/ModuleMapLoader.java:148-164` (`packages()`); no case in `ModuleMapLoaderTest.java`.
- **Evidence:** `specify/spec.md:114` (field matrix, `modules[].published`) requires "unique per module", and SPEC-002 says the map follows that matrix. `packages()` checks the pattern and the internal-package ban but not uniqueness, so `[api, api]` loads. Uniqueness is checked and tested for `code`, module `name`, external `name` and `clientLibraries`. No deviation records the gap.
- **Effect:** none on boundary decisions today (`PUBLISHED_PACKAGES` is a `Set`), but a map that breaks a gated constraint is accepted silently (BR6, fail closed).
- **Required fix:** reject a repeated entry within one list, naming the field path and "duplicate value"; add `duplicatePublishedIsRejected`, red then green. Or record a deviation that drops the constraint.

### CONF-TE001-02 (Low): a test comment and plan addendum A-4 claim a detection the test does not make

- **Where:** `RecoveryBoundaryTest.java:109-110`; `plan/plan-addendum.md:71-73` (A-4).
- **Evidence:** both say a package that gains a public type without being published, or is missing from the map, fails the exact comparison. The loop at `RecoveryBoundaryTest.java:119-125` skips any package not in `PUBLISHED_PACKAGES`, so such a type is never compared. Only a new public type in an already published package is caught. Cross-module use of such a type is still caught by BND-1/BND-2, Modulith verify and the module-map rule, so the behaviour is acceptable, but the record overstates SPEC-025 coverage. Code gate round 2 accepted CODE-005 on this wording.
- **Required fix:** correct the comment and A-4 (append-only note in the addendum) to say what the test covers. Or extend the test so a public type in a non-published, non-internal package fails, red then green.

## 8. Already registered elsewhere (not counted here)

| Item | Registered as |
|---|---|
| Commits and merge `dc2d25b` name Claude Code / Opus 5.5, but most of the build ran in opencode on DeepSeek v4.1 Flash | evidence-audit H-03; D-RUN-26 |
| No named human approver for the merge | evidence-audit H-01; OPEN-016, OPEN-054 |
| TE-001 Thai mojibake not in AGENTS §11 | evidence-audit H-04 |
| No log rows for the TE-001 API and functional tests | evidence-audit H-06 |
| INC-002 README errors | evidence-audit L-01 |
| Coverage verification not in CI | REVIEW-001 H3 |
| Literal role names in moved controllers | REVIEW-001 L10 |

## 9. Verdict

The merged code meets AC1..AC7 and BR1..BR6. Every boundary rule has a must-fail fixture with exact
assertions, no test was weakened or skipped, and the evidence figures match their files. Two Low findings
remain; under D-RUN-09 the gate fails until both are fixed (or recorded as deviations) and re-reviewed.

REVIEW_TYPE: CODE_GATE_REVIEW (CONFIRMATION)
CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
