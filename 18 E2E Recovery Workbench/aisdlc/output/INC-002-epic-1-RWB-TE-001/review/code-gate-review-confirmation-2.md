# Code gate review (confirmation, round 2): RWB-TE-001

| Field | Value |
|---|---|
| Run | `INC-002-epic-1-RWB-TE-001` |
| Scope | Re-gate of CONF-TE001-01 and CONF-TE001-02 from `code-gate-review-confirmation.md`, plus any new finding in the TE-001 files changed on the REVIEW-001 branch |
| Branch | `fix/REVIEW-001-post-merge-review`, diff `27567ed..cd2dffa` (code tip `5679889`) |
| Reviewer | Compliance Reviewer, code gate mode, on Claude Opus 5.5, high effort. Read only |
| Date | 19 Nov 2026 |
| Tests | My run of `./gradlew cleanTest test recoveryCoverageVerification` at `cd2dffa`: 430 tests, 0 failed, coverage verification passed |
| Rule | D-RUN-09: any finding, Low included, fails the gate |

## 1. Earlier findings

| Finding | Status | Evidence |
|---|---|---|
| CONF-TE001-01 duplicate `published` entry accepted | Closed | `ModuleMapLoader.java:152,162-165` rejects a repeated entry in `modules[].published` and `external[].published` with the field path and "duplicate value". `clientPackages` is left alone, as the spec field matrix requires uniqueness for `published` only (D-11). `ModuleMapLoaderTest#duplicatePublishedIsRejected` covers both lists. Red `1a44389` (fails on the old loader), green `61aefc3` |
| CONF-TE001-02 comment and A-4 overstate the test | Closed | `RecoveryBoundaryTest.java:109-113` now says the test compares published packages only and that a type in an unpublished package is caught by BND-1/BND-2, Modulith verify and the module-map rule. `plan/plan-addendum.md` A-4 has a dated append-only correction; the original text is unchanged. The test is unchanged. Commit `8701e7d`. One count in the same comment is still wrong: CONF2-TE001-01 |

## 2. Other TE-001 files in the diff

- `.gitlab-ci.yml` `backend-unit` now runs `recoveryCoverageVerification` (REVIEW-001 H3). No finding.
- `PlatformInfoProperties.java` (SPEC-023) validates `rwb.environment` against DEV/SIT/UAT/PROD with no default
  (REVIEW-001 H2); `PlatformInfoControllerTest` now supplies the value and adds a missing-value and a wrong-case
  test. Not weakened. No finding.
- `App.tsx` and `AuthCallback.test.tsx` (REVIEW-001 M11, committed under RWB-TE-001): the code is correct. The
  missing red commit is counted once, as CG-R001-05 in `REVIEW-001-first-four-stories/review/code-gate-review.md`,
  not here.

## 3. New finding

| ID | Severity | Where | Defect | Required fix |
|---|---|---|---|---|
| CONF2-TE001-01 | Low | `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryBoundaryTest.java:113-117` | The comment rewritten for CONF-TE001-02 says "The six type-bearing packages are asserted", but the assertion lists seven (`casewf.config.api` was added by RWB-E1-042). Same defect as CG-R001-04 in the REVIEW-001 gate | Say "seven", or drop the count |

## 4. Verdict

Both earlier findings are closed. One Low finding remains in the corrected comment, so under D-RUN-09 this
confirmation gate fails until it is fixed and re-reviewed.

CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 1]
