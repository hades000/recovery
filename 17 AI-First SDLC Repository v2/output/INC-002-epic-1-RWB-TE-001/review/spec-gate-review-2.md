# Spec gate re-review (gate 2): RWB-TE-001 (INC-002-epic-1-RWB-TE-001)

| Field | Value |
|---|---|
| Review type | SPEC GATE RE-REVIEW (gate 2, specification stage) |
| Story | RWB-TE-001 (Jira `TB0001-1235`) |
| Reviewer | Compliance Reviewer (agent run), 2026-11-09 |
| Gate 1 report | `output/INC-002-epic-1-RWB-TE-001/review/spec-gate-review.md` (REVIEW-RWB-TE-001-004..014: 3 Medium, 8 Low) |
| Tech-lead rulings applied | 2026-11-09: 004 close the gap in the map rule; 005 alias `@/modules/recovery/**` + `./`, ban every `../`, no new ESLint plugin; 006 native coverage (JaCoCo + `@vitest/coverage-v8`); 014 record as D-RCV-38+ |
| Artifacts reviewed | `specify/spec.md` (SPEC-RWB-TE-001-001..020), `specify/compliance-validation.md` §4, `specify/contracts/backend-apis.json`, `specify/contracts/frontend-integrations.json`, `requirement/Traceability_Matrix.md` rows 111, 122, 125, 141, 338, `docs/increments/INC-002-epic-1-RWB-TE-001.md`, `docs/decisions/INC-001-decisions.md` (D-RCV-38..42), `docs/open-items.md`, `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` SPEC-RWB-E1-044-015 |
| ACE evidence (read-only) | `ace-monorepo` `develop` 96b0d1c6: `nx.json`, root `package.json` / `package-lock.json`, `frontend/package.json`, `frontend/tsconfig.app.json`, `frontend/tsconfig.node.json`, `frontend/eslint.config.js`, `frontend/vite.config.ts`, `frontend/src/{utils,lib,contexts}`, `.gitlab-ci.yml:33-62`, `backend/build.gradle.kts` (no `jacoco`); published package `@nx/vite@24.0.3` (`dist/src/plugins/plugin.js`, `plugin.d.ts`, `migrations/update-23-0-0/ensure-vitest-package-migration.md`) |
| Overall status | **FAIL** |
| Blocking | **YES**: 1 Medium finding (REVIEW-RWB-TE-001-015) |

## Disposition of gate 1 findings

| Finding | Sev. | Disposition | Evidence |
|---|---|---|---|
| REVIEW-RWB-TE-001-004 | Medium | **Resolved** | SPEC-004 (a) now covers packages holding classes only in sub-packages; new (e) bans public types in a module base package; new (f) bans type-level `@NamedInterface` under the root (`spec.md:145`). T-TE001-02 adds the three cases plus a non-public base-package pass case (`spec.md:218`). Contract MAP checks updated (`backend-apis.json` MAP rule). SPEC-007 and BR3 row reference (e)/(f) (`spec.md:51`, `:148`). Ruling recorded as D-RCV-42. |
| REVIEW-RWB-TE-001-005 | Medium | **Resolved** | SPEC-014 is stated on import text: `@/modules/recovery/...` and `./...` allowed, every `../` forbidden, other `@/modules/**` forbidden (`spec.md:155`). The contract matches (`frontend-integrations.json:20-40`) and D-RCV-39 matches. T-TE001-07 now uses `../x` and `../../hooks/cfsc/x` as rejected cases and `./sibling`, `@/modules/recovery/casewf/x` as accepted ones (`spec.md:224`). No new ESLint plugin. Every allowed path exists in ACE (`src/lib/utils.ts`, `src/contexts/ApiClientContext.ts`, `src/utils/date.ts`; `cfsc*` files present to exclude). The ACE ESLint config is not type-aware (`tseslint.configs.recommended`, no `parserOptions.project`), so excluding `__tests__` from `tsconfig.app.json` does not break lint. |
| REVIEW-RWB-TE-001-006 | Medium | **Resolved** (residual gaps in new REVIEW-016, -017) | Native coverage is planned in SPEC-020 (`spec.md:161`): JaCoCo `recoveryCoverageReport` / `recoveryCoverageVerification` at 80% LINE/INSTRUCTION/BRANCH/METHOD over the recovery packages plus the test-scope `ModuleMapLoader` and rule factory, and `@vitest/coverage-v8` at 80% with thresholds in `vitest.config.ts`. Both Unit Test Applicability rows are `YES`/`REQUIRED` with no non-gate outcome (`spec.md:135-136`). T-TE001-10 added. Measuring test-scope tooling as the backend scope is a deviation from "production-source scope" that D-RCV-40 explicitly approves. |
| REVIEW-RWB-TE-001-007 | Low | **Resolved** | Name-boundary match (`e`, `e.`, `e$`) in SPEC-009 (`spec.md:150`), the field matrix (`:93`), contract `clientLibraries.meaning` (`backend-apis.json:96`) and D-RCV-41; T-TE001-09 (`spec.md:219`). |
| REVIEW-RWB-TE-001-008 | Low | **Resolved** | SPEC-007 states the Modulith cycle check and credits the event-type rule to Modulith behaviour under D-RCV-11 (`spec.md:148`); contract BND-3 notes; D-RCV-42. |
| REVIEW-RWB-TE-001-009 | Low | **Resolved** | Field matrix (`spec.md:87`) and contract `sharedPackages` (`backend-apis.json:99`) record that RWB-TE-003 extends the schema, loader and MAP (a). |
| REVIEW-RWB-TE-001-010 | Low | **Resolved for items (1)-(3); item (4) superseded by REVIEW-RWB-TE-001-015** | Lockfiles are in SPEC-017 and the contract `sharedFiles`. `ignore: false` is in SPEC-015. `__tests__` and `__fixtures__` are excluded from `tsconfig.app.json`. Item (4) of gate 1 said `@nx/vite/plugin` "can infer a `test` target". That statement was wrong for ACE's Nx 24.0.3 (reviewer error at gate 1). The remediation followed it, see REVIEW-015. |
| REVIEW-RWB-TE-001-011 | Low | **Resolved** | MR job `nx affected -t check`, default-branch job `nx run-many -t check` in the header, Trigger, Inherited behaviour, Flow 6, CLAR-009 and the contract (`spec.md:20`, `:37`, `:58`, `:75`, `:261`; `backend-apis.json` `runIn`); matches `.gitlab-ci.yml:43`, `:62`. |
| REVIEW-RWB-TE-001-012 | Low | **Resolved** | Matrix row 122 (CTX-CONSTRAINT-002) and row 125 (CTX-CONSTRAINT-005 / FR-RWB-003) link SPEC IDs consistent with the spec Traceability table (`spec.md:244-245`). Row 338 shows "PENDING (gate 1 FAIL ..., re-review pending)". This is acceptable because the matrix has no review-finding column. |
| REVIEW-RWB-TE-001-013 | Low | **Resolved** | Card flow step 5 struck through for D-RCV-36, step 2 for D-RCV-37 and step 6 for D-RCV-05. Status rows read "re-specified 2026-11-09" and "gate 1 FAIL ... re-review pending". The deleted run-log link is replaced by the review report link (`INC-002...md:35-39`, `:142`, `:150-151`). |
| REVIEW-RWB-TE-001-014 | Low | **Resolved** (residual in REVIEW-018) | D-RCV-38..42 are in `docs/decisions/INC-001-decisions.md:74-78`, and the next free number is D-RCV-43 (`:35`). The CLAR-to-decision mapping in `spec.md:266` matches. The open-items part of the gate 1 fix was not done, see REVIEW-018. |

Earlier findings REVIEW-RWB-TE-001-001 and -003 (Low) stay open and visible as before. Their dispositions are unchanged in `compliance-validation.md` §3.

## New findings

| ID | Severity | Location | Maps to | Issue | Required fix |
|---|---|---|---|---|---|
| REVIEW-RWB-TE-001-015 | Medium | `spec.md:156` (SPEC-015), `spec.md:158` (SPEC-017), `contracts/frontend-integrations.json:34`, `docs/decisions/INC-001-decisions.md:76` (D-RCV-40) | SPEC-015, -017, -020; T-TE001-08; D-RCV-40; CLAUDE.md shared-file rule | The frontend `test` target will not exist. SPEC-015 and D-RCV-40 say the target "is the one the `@nx/vite/plugin` infers from `frontend/vitest.config.ts`" and tell the plan not to hand-define one. ACE runs Nx 24.0.3 (root `package.json:20`). Vitest target inference was removed from `@nx/vite/plugin` in Nx 23 and moved to the separate `@nx/vitest` plugin (`@nx/vite@24.0.3` `migrations/update-23-0-0/ensure-vitest-package-migration.md`). `dist/src/plugins/plugin.js` creates only build, serve/dev, preview, serve-static and typecheck targets, and `VitePluginOptions` has no `testTargetName`. `nx.json` registers no `@nx/vitest` plugin. So `test` in `check.dependsOn` names a missing target. Either `check` errors, or the boundary fixture test and the frontend coverage report never run in CI (§13 step 5 proof and the D-RCV-40 gate). Neither fix is in the approved footprint: registering `@nx/vitest` edits root `nx.json`, a workspace-wide shared file that SPEC-017 does not list, and a hand-defined target is forbidden by SPEC-015. The plan would have to invent the wiring. Gate 1 REVIEW-010 item (4) caused this: the reviewer stated the inference as fact without checking the Nx version. | The recovery tech lead picks one option and records it in D-RCV-40 (amend) or D-RCV-43. (a) Register `{ "plugin": "@nx/vitest", "options": { "testTargetName": "test" } }` in root `nx.json`. `@nx/vitest@24.0.3` is already in the root lockfile as a dependency of `@nx/vite`. Declare it in root `devDependencies` and add `nx.json` and root `package.json` to SPEC-017 and the contract `sharedFiles`. This option also affects any other project with a vitest config. (b) Hand-define `test` in `frontend/package.json` `nx.targets` (for example `vitest run --coverage`, with inputs and outputs), with no `nx.json` change. Then update SPEC-015, SPEC-017, `frontend-integrations.json` `wiring` and D-RCV-40 to match. Under either option the plan proves the target with `npx nx show project frontend`. |
| REVIEW-RWB-TE-001-016 | Low | `spec.md:135` (Unit Test Applicability, Frontend), `spec.md:161` (SPEC-020), `spec.md:154` (SPEC-013) | SPEC-013, -020; `.github/rules/implementation-execution-gates.md` results table | The frontend coverage scope holds no measurable code. After excluding `__tests__` and `__fixtures__`, the include `src/modules/recovery/**/*.{ts,tsx}` covers only the SPEC-013 placeholder, which "holds no runtime code". If that file is not `.ts`/`.tsx`, the scope holds no file at all. The report will show 0 statements, branches and functions. Depending on the reporter, the tool prints `Unknown` or 100%, and the threshold check is vacuous. The logic under test (the recovery block in `frontend/eslint.config.js`) is outside the measured scope. SPEC-020 says only "records the tool's measured output as printed". It does not say which gate status (`PASS`, `BLOCKED`, `NOT_SUPPORTED`) the Implementation Builder reports for a 0/0 surface. The Builder would decide that alone at the hard gate. | State in SPEC-020 and the Frontend applicability row the expected result for this story: the row is `PASS` when tests pass and the native report shows 0 measurable statements in the declared scope, recorded as printed with the file list, on the basis of D-RCV-40. Also state that the rule's correctness is proven by T-TE001-07, not by a coverage figure. Alternatively, name a real measurable frontend scope. |
| REVIEW-RWB-TE-001-017 | Low | `spec.md:35` (Impacted Existing Nodes), `spec.md:158` (SPEC-017), `spec.md:161` (SPEC-020), `contracts/backend-apis.json:380-382`; `output/INC-001-epic-1-RWB-E1-044/specify/spec.md:163` (SPEC-RWB-E1-044-015 (d)) | SPEC-017, -020; D-RCV-40; CLAUDE.md shared-file rule | The two merge orders are not both covered. SPEC-017 and the Impacted Nodes row touch `backend/build.gradle.kts` only "if RWB-E1-044 has not merged [the JaCoCo tasks] first", and SPEC-020 says "the other reuses them". RWB-E1-044 defines the tasks over `th/co/scb/ace/demo/recovery/**` main classes only, while SPEC-020 / D-RCV-40 require TE-001's tasks to include the test-scope boundary tooling (`ModuleMapLoader`, rule factory). (1) If E1-044 merges first and TE-001 "reuses" its tasks unchanged, the tooling is not measured. The backend report then has zero executable lines and the 80% rule passes on nothing. Adding the test class directory needs a `build.gradle.kts` edit that SPEC-017 excludes in that case. (2) If TE-001 merges first, E1-044 inherits tasks that also measure test tooling and run without `recoveryIntegrationTest`. E1-044's spec does not say this. | In SPEC-017 and SPEC-020, state that TE-001 always edits `backend/build.gradle.kts` for coverage. If the tasks exist, TE-001 adds the boundary-tooling class directory from the test source set. If they do not, TE-001 creates them as in SPEC-RWB-E1-044-015 (d) plus that directory. Report the scope change to RWB-E1-044 for its plan (Context Updater or Technical Specifier of INC-001). Update the contract `addedBy` text to match. |
| REVIEW-RWB-TE-001-018 | Low | `docs/open-items.md` (no RWB-TE-001 entry), `compliance-validation.md:30`, `:33-42`; `docs/decisions/INC-001-decisions.md:72-78` ("who must act" column) | REVIEW-014 residual; CLAUDE.md ("Items waiting on an owner outside the run are in `docs/open-items.md`") | Actions owed by people outside the run appear only in the decisions register and in `compliance-validation.md`. None is in the open-items register. The missing items are: BA story-text updates for D-RCV-36, -37, -39 and -42 (§4, §5 X7, §12, §13, §14, §16); Context Updater alignment of FS-1.2 and frontend-context §Host (D-RCV-39); ACE tech lead approval of the new build dependencies and shared files (D-RCV-40: `vitest`, `@vitest/coverage-v8`, JaCoCo plugin); and the ACE team naming the common and collection roots (D-RCV-41, DL05). Gate 1 REVIEW-014 asked for the open-items entries. Without them, OPEN-* tracking misses these items. | Add OPEN-021 onward to `docs/open-items.md` for each owner action above, with stories affected, owner, needed-by date and a link to the decision. The ACE tech lead approval is needed by plan approval. |

## Consistency checks (no finding)

| Check | Result |
|---|---|
| Spec ↔ decisions D-RCV-38..42 | Consistent apart from the `@nx/vite/plugin` text in D-RCV-40 (REVIEW-015). The allow-list in SPEC-014, D-RCV-39 and the contract is identical. The 16 client libraries are identical in the spec, contract and D-RCV-41. |
| Spec ↔ contracts | MAP checks (a)-(f), BND-1..5, coverage block, frontend allow-list and wiring all match the spec. |
| SPEC ID range | SPEC-001..020, each defined once. The matrix (rows 111, 338) and `compliance-validation.md` say 001..020. |
| Stale references | None found for the access guard, `nx affected` on the default branch, D-RCV-20 event attribution or the run log. Story-text items in compliance-validation §2 are labelled as BA actions. |
| Coverage approach vs `implementation-execution-gates.md` | Native reports, 80% on all four metrics, thresholds in the runner config, required surfaces separate. The backend scope deviation is approved by D-RCV-40. The frontend 0/0 status and the E1-044 merge order are open (REVIEW-016, -017). The frontend runner wiring blocks (REVIEW-015). |
| Gate status line | `CONTRADICTIONS: 0` in `spec.md:276` is not accurate while REVIEW-015 stands (spec says inferred target; ACE cannot infer it). Re-check after remediation. |
| PII, secrets, production data | None in the spec, contracts, decisions or this report. |
| Authorization, audit, KYC/AML | N/A: no runtime code or endpoint (D-RCV-36). Accepted. |
| Design evidence | `NOT_REQUIRED` (UI NO). Accepted. |

## Required checks summary

| Check | Result |
|---|---|
| Authentication / authorization | N/A (D-RCV-36) |
| Customer / account data protection | PASS |
| Audit logging | N/A |
| KYC/AML/suitability/consent/approval | N/A |
| Frontend integration versioning / error contract | N/A for API. The lint contract is encodable (REVIEW-005 resolved); runner wiring is wrong (REVIEW-015). |
| Secrets and environment configuration | PASS |
| Requirement-to-SPEC coverage | 6/6 BRs; BR3 gap closed |
| Unit-test gates planned | Partly. Native coverage is planned, but the frontend test target is not wireable as written (REVIEW-015). The 0/0 status (REVIEW-016) and the E1-044 merge order (REVIEW-017) are open. |
| Traceability | PASS (REVIEW-012 resolved) |
| Open-items tracking | Partly (REVIEW-018) |

## Status lines

```text
REVIEW_STATUS: FAIL
REVIEW_TYPE: SPEC_GATE_RE_REVIEW
RUN_ID: INC-002-epic-1-RWB-TE-001
GATE1_FINDINGS: [RESOLVED: 11] [NOT_RESOLVED: 0] (REVIEW-RWB-TE-001-004..014; 010 item 4 superseded by 015, 006 and 014 residuals in 016..018)
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 3]
REVIEW_BLOCKING: YES [REASON: Medium finding REVIEW-RWB-TE-001-015 (frontend test target not inferable under Nx 24) requires a tech-lead choice, remediation and re-review, or explicit human acceptance]
NEXT_STEP: Human disposition of REVIEW-RWB-TE-001-015..-018; recovery tech lead chooses the test-target wiring (nx.json @nx/vitest plugin or hand-defined target); re-run Technical Specifier for remediation, then re-run the spec gate review. Do not start Implementation Planner.
```

No `REVIEW_GATE_WARNING`: the review has a Medium finding, so the handoff is blocked. The Low-only warning does not apply.
