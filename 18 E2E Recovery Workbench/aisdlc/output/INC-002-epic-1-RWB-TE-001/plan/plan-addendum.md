---
title: "Plan addendum: RWB-TE-001 post-gate change record"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
stage: "plan addendum (change record, not a plan revision)"
date: "2026-11-18"
status: "APPLIED"
---

# Plan addendum: RWB-TE-001

This addendum records changes made after the plan and spec gates passed. It does **not** edit the
gated `../specify/spec.md` v4 or `plan.md`/`tasks.md` v7; those stay as approved. It is the change
record the code gate asked for (CODE-002, CODE-004, CODE-008) and carries the rationale and evidence
for each deviation. The story branch tip after the code-gate fix is `55f1ed4`.

## A-1. `frontend/eslint.config.js` tightened (CODE-002, DEV-08; SPEC-014, AC6, D-RCV-39)

**What changed.** The D-RCV-39 `recoveryImportRule` gains one pattern:

```js
{ regex: "^(?!\\.\\./).*\\.\\.", message: "D-RCV-39: no '..' path segments in the recovery module." }
```

**Why.** The security review (SEC-TE001-01, Medium) showed that the allow-list could be bypassed by
hiding `..` behind an allowed prefix: `@/components/ui/../../modules/collection/worklist/WorkList`,
`@/modules/recovery/../../collection/worklist/WorkList` and `./../collection/worklist/WorkList` all
resolved outside the recovery folder while the old patterns stayed silent. The leading-`../` group
already reports specifiers that start with `..`, so the negative lookahead excludes that form and
keeps one diagnostic per import; the union of the two patterns rejects every specifier that contains
a `..` segment. No existing pattern was removed or weakened.

**Why plan.md said "unchanged".** Plan v7 line 229 listed `frontend/eslint.config.js` as unchanged
because the inherited rule met AC6 as specified. The code gate accepted the tightening as a
recovery-scoped security fix (DEV-08); it is a strict superset of the approved rule.

**Evidence.** `../../implement/frontend/review1-red.log` (three new cases rejected before the rule),
`../../implement/frontend/review1-vitest.log` (18/18), `../../implement/frontend/review1-check.log`
(`npm run check` 28/28, `eslint .` green), `../../implement/frontend/review1-build.log`.

## A-2. Two extra test-only files (CODE-004, DEV-05, DEV-06)

| File | Why it exists | Why it is not in plan v7 | Evidence |
|---|---|---|---|
| `backend/src/test/java/th/co/scb/ace/demo/recovery/casewf/rules/RuleFactsTest.java` | SPEC-024 says any class still under 0.80 gets a test at its home. `RuleInput`, `RuleOutcome` and `RuleResult` were at 69%, 90% and 33% line coverage after the named eleven tests. | The plan's "Coverage tests" table names eleven classes; these three value types were not listed. | 4/4 pass; `backend/review1-suites.txt`; JaCoCo per-class counters in `backend/coverage/recoveryCoverageReport.xml` |
| `backend/src/test/java/th/co/scb/ace/boundaryfixture/mapbad/recovery/casewf/events/CaseEventType.java` | Gives the `mapbad` world a second class in the listed-but-unannotated `casewf.events` package, so the rule's "one line per distinct violation" dedupe path is exercised. The expected `mapbad` output stays at eight lines. | The `mapbad` fixture description names `CaseEvent` only. | `BoundaryRulesTest.mapViolationsAreAllReported` (8 lines), `BoundaryRulesTest` 17/17 |

Both files are test scope only, carry no business value or personal data, and are excluded from the
JaCoCo class directories by the existing include/exclude rules (fixtures and `*Test` classes).

## A-3. Import-boundary test has 18 cases, not the spec's 15 (CODE-008, DEV-08; SPEC-015, AC6)

SPEC-015 and `tests/scenarios.md` T-TE001-07 describe 8 rejected + 7 allowed = 15 fixture imports.
The committed test has **11 rejected + 7 allowed = 18**: the review fix added the three `..` bypass
forms from A-1.

| Added rejected case | Relation to SPEC-015 |
|---|---|
| `@/components/ui/../../modules/collection/worklist/WorkList` | `..` behind an allowed `@/components/ui/` prefix |
| `@/modules/recovery/../../collection/worklist/WorkList` | `..` behind the allowed `@/modules/recovery/` prefix |
| `./../collection/worklist/WorkList` | `..` behind `./` (the old `../` group only matches a leading `../`) |

The test is **stronger** than the plan, not weaker: the original 15 cases are unchanged and all pass.
`functional-tests/report.md` FAT-OBS-02 records the same drift.

## A-4. Published-surface test strength (CODE-005, CODE-006)

- `RecoveryBoundaryTest.PUBLISHED_PACKAGES` is now derived from the module map
  (`MAP.modules()` × `published` entries) instead of a literal set, so the map is the only source of
  published package names (BR6). The exact per-package type list is unchanged. The test asserts that
  the derived set still contains the six type-bearing packages, so a map that drops one fails here;
  a published package that gains a public type, or a package with types that is missing from the map,
  changes the compared map and fails the exact comparison (fail closed).
- `casewfNamedInterfacesAreTheSpecifiedBoundedSet` now asserts `api` as well as `rules`, `timers` and
  `workflow`. Spring Modulith 2.1.1 **does** report `casewf.api` even though the package holds no
  type today (only the annotated `package-info`), so no exclusion had to be recorded. Plan input
  R3-1's unnamed base-package interface stays filtered by `isUnnamed()`.

Evidence: `../../implement/backend/codegate-code005-006.log` (`RecoveryBoundaryTest` 11/11).

**Correction, 2026-11-19 (REVIEW-001, CONF-TE001-02; append-only, the text above is unchanged).**
The first bullet of A-4 overstates the test. `publishedSurfaceIsExactlyTheSpecifiedTypes` compares
the exact public types of every package the map publishes, so a new public type in a published
package fails it. It skips packages the map does not publish: a package that gains a public type
without being published, or a package with types that is missing from the map, is not compared.
Such a type is caught instead by BND-1/BND-2, Modulith verify and the module-map rule when another
module uses it. The comment at `RecoveryBoundaryTest.java` was corrected to say the same.

## Not fixed here

CODE-001 (e2e regression) and CODE-007 (`dev.ps1 test` at the final tip) are owned by the
orchestrator per the code-gate disposition. This addendum records only the builder-side changes.
