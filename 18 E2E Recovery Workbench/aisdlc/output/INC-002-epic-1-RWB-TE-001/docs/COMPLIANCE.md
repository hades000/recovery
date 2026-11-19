---
title: "RWB-TE-001 Recovery module and boundary test — compliance record"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED — code gate PASS; no merge, human approval or release claimed"
---

# Compliance record — RWB-TE-001

This record states what the story demonstrates, with the evidence that demonstrates it. It is
written after the code gate passed (round 2, PASS 0/0/0/0) and does not add a new review.

## 1. Scope of this record

| Field | Value |
|---|---|
| Story | RWB-TE-001 Recovery module folder and boundary test, EPIC-001, module P2 Integration |
| Acceptance basis | AC1–AC7 and BR1–BR6 of the story file v7, RWB-TE-001 v1 (D-RCV-51) |
| Change classification | `NEW_STORY`; UI In Scope `NO`; API In Scope `NO`; `NO_API_CHANGE` |
| Runtime behaviour | None added. Package relocation only, with unchanged behaviour |
| Personal data | None. Class, package and synthetic names only; no production data anywhere |
| Banking compliance documentation | Not required by the requirements: no customer data, no business rule, no financial value, no account or card field in this story |

## 2. Acceptance criteria and business-rule trace

**DOC ID:** DOC-RWB-TE-001-011 · **Maps to:** AC1–AC7, BR1–BR6, TASK-03..-09, TASK-11, TASK-15, TASK-16

### Acceptance criteria

| ID | Requirement (story file v7) | SPEC | TASK | Test evidence | Result |
|---|---|---|---|---|---|
| AC1 | A `recovery.casewf.internal.SampleService` importing `collection.internal.CollectorRepository` fails; the log names BND-1, `SampleService` and `CollectorRepository`. | SPEC-005, -010, -011 | TASK-05, -06, -07 | `BoundaryRulesTest.collectionInternalDependencyBreaksBnd1`; `RecoveryBoundaryTest.bnd1CollectionBoundary` | **PASS** |
| AC2 | `SampleService` calling an interface in `common.api` passes. | SPEC-006, -011 | TASK-05, -06, -07 | `BoundaryRulesTest.commonApiDependencyPassesEveryRule`; `BoundaryRulesTest.commonInternalDependencyBreaksBnd2` (control); `RecoveryBoundaryTest.bnd2CommonBoundary` | **PASS** |
| AC3 | A `recovery.integration.internal` class importing `recovery.decision.internal.DecisionLogRepository` fails with BND-3; importing published `recovery.decision.writer.DecisionLogWriter` passes. | SPEC-007, -011 | TASK-08 | `ModulithFixtureTest.internalDependencyBetweenModulesFailsVerify`, `.publishedWriterDependencyPassesVerify`, `.cycleBetweenModulesFailsVerify`; `ModulithTest.modulesRespectTheirBoundaries`; `BoundaryRulesTest.publishedWriterMatchesTheFixtureMap` | **PASS with accepted deviation D-RCV-42** (Modulith's own failure text) |
| AC4 | A `recovery.integration.internal` class using entity `recovery.casewf.internal.RecoveryCaseEntity` fails with BND-4. | SPEC-008, -011 | TASK-05, -06, -07 | `BoundaryRulesTest.foreignEntityAndRepositoryBreakBnd4`; `RecoveryBoundaryTest.bnd4EntitiesAndRepositoriesStayInTheirModule` | **PASS** |
| AC5 | `java.net.http.HttpClient` in `recovery.casewf.internal` fails BND-5; in `recovery.integration.adapter` it passes. | SPEC-009, -011 | TASK-05, -06, -07 | `BoundaryRulesTest.clientLibraryOutsideClientPackageBreaksBnd5`, `.clientLibraryMatchesOnANameBoundary`, `.matchesClientLibraryTable`; `RecoveryBoundaryTest.bnd5ClientLibrariesOnlyInClientPackages`; T-TE001-13 run 1 | **PASS** |
| AC6 | A component in `src/modules/recovery/caselist` importing the collection `WorkList` fails the frontend rule. | SPEC-014, -015 | TASK-15, -16 | `importBoundary.test.ts` — 11 rejected forms including both AC6 forms; 7 allowed forms; 18/18 | **PASS with accepted deviation D-RCV-39** (rule name and `@/` alias) |
| AC7 | A new package `recovery.vendorx` not in the map fails with `package recovery.vendorx is not in the module map`. | SPEC-003, -004, -010 | TASK-03, -04, -06, -07 | `BoundaryRulesTest.packageMissingFromTheMapFails`; `ModuleMapLoaderTest` (28 tests, including the real-map test); `RecoveryBoundaryTest.moduleMapRule` | **PASS** |

`X7` / TC-TE-001-08 (the 403 `MSG-P4-002` access guard) is **moved out of scope** to RWB-E1-022 by
D-RCV-52; the code gate checked that it is not built. It is not a gap in this story.

### Business rules

| ID | Rule (story file v7) | SPEC | TASK | Test evidence | Result |
|---|---|---|---|---|---|
| BR1 | BND-1: collection only through its published packages. | SPEC-005 | TASK-05, -06, -07 | AC1 tests; `BoundaryRulesTest.emptyExternalRootsPass` (T-TE001-03); `.allViolationsOfARuleInOneRun` (T-TE001-04); `RecoveryBoundaryTest.bnd1CollectionBoundary` | **PASS** |
| BR2 | BND-2: common only through its published packages. | SPEC-006 | TASK-05, -06, -07 | AC2 tests; `BoundaryRulesTest.commonInternalDependencyBreaksBnd2`; `RecoveryBoundaryTest.bnd2CommonBoundary` | **PASS** |
| BR3 | BND-3: another recovery module only through a published package or an application event. | SPEC-004 (d)–(f), -007 | TASK-08, -09, -13 | `ModulithTest.modulesRespectTheirBoundaries` (unchanged); three `ModulithFixtureTest` worlds; `RecoveryBoundaryTest.publishedSurfaceIsExactlyTheSpecifiedTypes` | **PASS** (D-RCV-42) |
| BR4 | BND-4: entities and repositories used only inside their module. | SPEC-008 | TASK-05, -06, -07 | AC4 tests; `RecoveryBoundaryTest.bnd4EntitiesAndRepositoriesStayInTheirModule` | **PASS** |
| BR5 | BND-5: client libraries only in map-allowed client packages; no recovery class calls a system of record. | SPEC-009, -010, -022 | TASK-05, -06, -07, -17 | AC5 tests; `RecoveryBoundaryTest.bnd5ClientLibrariesOnlyInClientPackages`; T-TE001-13 run 1 (`Rule BND-5 broken: … BoundaryProbe depends on java.net.http.HttpClient`, non-zero exit) | **PASS** |
| BR6 | Names, packages and published packages come from the map, not the test. | SPEC-002..-004, -026 | TASK-02, -03, -04, -09 | `ModuleMapLoaderTest`; `BoundaryRulesTest.toolingHoldsNoRecoveryPackageLiteral` and its self-test; `RecoveryBoundaryTest` derives `PUBLISHED_PACKAGES` from the map (code-gate CODE-005) | **PASS** |

Requirement-level trace: REQ-DRI-006 (no direct system-of-record call) → BR5/AC5 → SPEC-009/-010/
-011/-022; CTX-CONSTRAINT-002 / CTX-DELIVERY-004 (modular monolith, build-time boundary) →
BR1–BR4/AC1–AC4/AC6 → SPEC-001/-004..-008/-010..-015/-022/-025/-026; BR-RWB-014 → FR-RWB-020 (no
hard-coded values) → BR6/AC7 → SPEC-002..-004.

## 3. Coverage evidence (80% × 4)

**DOC ID:** DOC-RWB-TE-001-012 · **Maps to:** SPEC-RWB-TE-001-020, SPEC-RWB-TE-001-024, TASK-01, TASK-12, TASK-16

The gate is bundle level over **all** main classes under `th/co/scb/ace/demo/recovery/**` plus the
test-scope tooling package `architecture/boundary/**`. Only test classes (`**/*Test.class`,
`**/*Test$*.class`), `RecoveryBoundaryTest` and the fixture root
`th/co/scb/ace/boundaryfixture/**` are outside the measured set. **No main class is excluded and no
threshold was lowered.** Frontend coverage is the inherited `src/modules/recovery/**` scope,
excluding `__tests__` and `i18n`; no exclusion was added.

| Surface | Metric | Measured | Required | Result |
|---|---|---|---|---|
| Backend (JaCoCo) | LINE | 97.46% (692/710) | 80% | **PASS** |
| Backend | INSTRUCTION (statements) | 97.31% (3656/3757) | 80% | **PASS** |
| Backend | BRANCH | 95.31% (244/256) | 80% | **PASS** |
| Backend | METHOD (functions) | 97.91% (187/191) | 80% | **PASS** |
| Frontend (Vitest v8) | Lines | 91.66% | 80% | **PASS** |
| Frontend | Statements | 91.89% | 80% | **PASS** |
| Frontend | Branches | 88.09% | 80% | **PASS** |
| Frontend | Functions | 82.35% | 80% | **PASS** |

Commands and artefacts:

| Surface | Command | Evidence |
|---|---|---|
| Backend | `./gradlew test recoveryCoverageVerification` | exit 0; `../implement/backend/coverage/recoveryCoverageReport.xml` and HTML; `../implement/backend/review1-green.log` |
| Backend | `./gradlew test` | 22 suites, 141 tests, 0 failures, 0 errors, 0 skipped; `../implement/backend/review1-suites.txt` |
| Frontend | `npm run check` | 28/28; `../implement/frontend/review1-check.log`, `../implement/frontend/coverage-summary.json`, `../implement/frontend/lcov.info` |
| Frontend | `npm run build` | exit 0; `../implement/frontend/review1-build.log` |

The final native JaCoCo XML figures above were verified by the code gate. The orchestrator's
independent re-run of the same gate reported LINE 97.47%, INSTRUCTION 97.32%, BRANCH 95.31% and
METHOD 97.92% with a slightly larger bundle (711 lines, 3762 instructions, 192 methods); both runs
clear 0.80 (`../implement/orchestrator-verify.md` runs 1–2; `../review/code-gate-review-2.md`).
Per-class note: `SecurityConfig` is 62.5% on branches (5/8) because the audience-validator branches
need a real token from the JWKS endpoint, which the test scope forbids; the bundle branch gate is
95.31%.

No test was disabled, skipped or weakened. `blobClientOnlyInDocumentsModule` was **replaced** by
BND-5 because the approved spec requires it (SPEC-009, SPEC-026); BND-5 covers 16 libraries instead
of one. The four moved tests keep their assertions; only their package and import lines changed, plus
two workbook rows in `DroolsRuleEngineTest`.

## 4. Review evidence

**DOC ID:** DOC-RWB-TE-001-013 · **Maps to:** SPEC-RWB-TE-001-019, TASK-18, AC6

### Gates

| Gate | Result | Reference |
|---|---|---|
| Spec gate, round 5 | **PASS** 0/0/0/0; 13/13 rules covered | `../review/spec-gate-review-5.md` |
| Plan gate, round 7 | **PASS** 0/0/0/0; one-module settlement confirmed | `../review/plan-gate-review-7.md` |
| Code gate, round 2 | **PASS** 0/0/0/0; round-1 CODE-001..-008 all closed | `../review/code-gate-review-2.md` |
| Security review | **PASS**; after the fix 0 Critical / 0 High / 0 Medium / 0 Low | `../review/security-review.md` |
| Ponytail review | **Ship**; findings 1–5 closed | `../review/ponytail-review.md` |

### The one Medium security finding, and its fix

**SEC-TE001-01 — D-RCV-39 import allow-list bypassed by `..` inside an allowed prefix (Medium).**
The inherited ESLint rule only rejected a specifier whose first segment was `../` or an `@/` import
outside the allow-list. Three forms resolved outside the recovery folder with a green pipeline:

```text
@/components/ui/../../modules/collection/worklist/WorkList
@/modules/recovery/../../collection/worklist/WorkList
./../collection/worklist/WorkList
```

The finder reproduced this against the real `eslint.config.js` with ESLint 9.39.5 `lintText`, not by
reading the regex. Impact: a recovery component could take a compile-time dependency on collection
internals — the violation AC6 exists to prevent — and the new AC6 test did not cover that hole.

**Fix.** `frontend/eslint.config.js` gained one pattern under `recoveryImportRule`:

```js
{ regex: "^(?!\\.\\./).*\\.\\.", message: "D-RCV-39: no '..' path segments in the recovery module." }
```

The leading-`../` group already reports that form, so the negative lookahead keeps one message per
import; the union of the two patterns rejects every specifier containing a `..` segment. No existing
pattern was removed or weakened, and no other config changed. Three rejected cases were added to
`importBoundary.test.ts`; all three failed before the rule (`../implement/frontend/review1-red.log`)
and pass after (`../implement/frontend/review1-vitest.log`, 18/18). The reviewer re-read the fix,
reproduced it against the real config over 19 specifiers, and closed the finding: **0 Critical,
0 High, 0 Medium, 0 Low** (`../review/security-review.md`, "Fix round 1 verification").

One residual note is cosmetic and one is a change-control note, neither a finding: the regex matches
any `..` substring rather than only a `..` path segment (e.g. `./a..b.ts`), and the fix edits a file
the gated plan listed as unchanged — recorded as DEV-08 and plan addendum A-1.

### Other review fixes carried by the branch

| Finding | Disposition |
|---|---|
| Ponytail Must 1: Thai `messageTh` re-encoded to mojibake in `ApiError`, three `§` comments corrupted | Fixed: `ApiError` restored from the base and now differs only in the `package` line; Thai text and `§` comments verified |
| Ponytail Must 2: BND-1/BND-2 accepted sub-packages of a published external package | Fixed: exact package comparison; new `bnd2` fixtures `SecretHelper` (fails) and `CustomerLookup` (passes) |
| Ponytail Should 3: Thai tests asserted only the Latin placeholder | Fixed: exact Thai `NOT_PERMITTED` string asserted |
| Ponytail Nice 4: five same-package imports | Fixed: removed |
| Ponytail Nice 5: unused `moduleFor` map parameter | Fixed: helper deleted |
| Ponytail follow-up 6: the new `..` pattern can double-report `@/api/schema/../x` | Cosmetic, documented; the import is still rejected, the three added bypass cases each get one message |
| Code gate CODE-001..-008 | All closed; CODE-001 (e2e) and CODE-007 (merge gate at the final tip) run by the orchestrator |

## 5. Accepted deviations

**DOC ID:** DOC-RWB-TE-001-014 · **Maps to:** AC3, AC6, SPEC-RWB-TE-001-007, SPEC-RWB-TE-001-014

| Decision | What it settles | Where it shows | Why it is acceptable |
|---|---|---|---|
| **D-RCV-42** | BND-3 is enforced by Spring Modulith `verify()` in the existing `ModulithTest`, with **Modulith's own failure text** and its cycle check instead of a bespoke `Rule BND-3 broken:` line. | AC3; SPEC-007; `ModulithFixtureTest` asserts failure and names `DecisionLogRepository`. | The recovery tech lead accepted it on 2026-11-09; one engine, no duplicated boundary logic; the module-map rule keeps `@NamedInterface` on `package-info` so the published surface still matches the map. |
| **D-RCV-39** | The frontend boundary is the inherited `no-restricted-imports` **allow-list**, not a rule named `no-collection-import`; the collection import is written `@/modules/collection/worklist/WorkList` or a `../../` path because this repository has no `src/modules/collection` and uses the `@/` alias (D-RCV-10). | AC6; SPEC-014; `importBoundary.test.ts` rejects both forms. | The rule is the ACE front-end rule, applied unchanged apart from the SEC-TE001-01 tightening; both AC6 forms are in the rejected set. |

Both deviations are recorded in the spec's Requirement-to-SPEC table and were re-checked by the code
gate. Neither is a defect and neither is hidden.

## 6. Open items and human verification

**DOC ID:** DOC-RWB-TE-001-015 · **Maps to:** SPEC-RWB-TE-001-012 (c), HV-01; TASK-18

| ID | Item | Status here | Consequence |
|---|---|---|---|
| **OPEN-016** | Per-story approver names are not available in Jira. | **OPEN.** No named approver, AGENTS.md §9 "Plan approved" sign-off or human acceptance is recorded or claimed in this run. The code gate's "Plan approved" row reads `NOT RECORDED`. | Human review and merge must supply the named approver. Documentation does not substitute for it. |
| **OPEN-050** | Define "module" in the one-module plan rule (ACE module or design module) and ratify D-RUN-18..D-RUN-21. | **OPEN — not ratified.** D-RUN-21 (orchestrator, 18 Nov 2026) settles the reading for this build as the ACE module (recovery); this story creates 19 nested design modules inside it. | A tech lead ratifies or replaces the reading. The plan gate confirms the settlement; it is not a human approval. |
| **HV-01** | The GitLab project blocks a merge request whose pipeline fails ("Pipelines must succeed"). | **OPEN — human.** No GitLab MCP is connected; not tested and never reported as tested. The local equivalent is proven by T-TE001-13 (`dev.ps1 test` exits non-zero on a real violation). | The ACE platform or DevOps owner checks the setting on the first merge request and records the result. |
| **A-09 / SU-10** | CI runs the coverage **report**, not the verification task. | **Deferred** to RWB-TE-003 / RWB-TE-011 by D-RCV-05; not a defect in this story. | The 80% gate is enforced by running `recoveryCoverageVerification`; wiring it into CI is later work. |

No approval, acceptance, ratification, release, SIT exit or UAT exit is claimed anywhere in this
document. The branch is ready for human review at `55f1ed4`; merge is a human action.

## 7. Change control after the gates

**Plan addendum A-1..A-4** (`../plan/plan-addendum.md`) records the post-gate changes without
editing the gated spec v4 or plan/tasks v7:

| Item | Change | Disposition |
|---|---|---|
| A-1 / DEV-08 | `frontend/eslint.config.js` tightened with the `..` rejection although plan v7 listed it as unchanged. | Disclosed; a strict superset of the approved rule, recovery-scoped; code gate accepted. |
| A-2 / DEV-05, DEV-06 | Two extra test-only files: `RuleFactsTest` and `mapbad.CaseEventType`. | Test scope only; no exclusion change; accepted. |
| A-3 / DEV-08 | The import test has 18 cases (11 + 7), not the spec's 15 (8 + 7). | Stronger than the plan; original 15 unchanged; accepted. |
| A-4 / CODE-005, CODE-006 | `PUBLISHED_PACKAGES` derived from the map; `casewf` named-interface assertion includes `api`. | Fail-closed strengthening; accepted. |

Other disclosed deviations (DEV-01..DEV-09, `../implement/deviations.md`) are build-process or
test-only corrections. DEV-01 (the builder could not start the local stack) is closed by the
orchestrator's e2e run, 6/6.

## 8. Statement

RWB-TE-001 is implemented and evidenced at branch tip `55f1ed4`. Every acceptance criterion and
business rule has a named test or an explicitly accepted deviation; backend and frontend coverage
clear 80% on all four metrics; the code gate and security review pass with no outstanding Critical,
High or Medium finding. Human review and merge remain outstanding (OPEN-016), host-side merge
blocking remains a human check (HV-01), and the one-module definition remains unratified (OPEN-050).
This document makes no release-readiness claim.
