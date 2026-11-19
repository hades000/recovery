---
title: "Technical Specification: RWB-TE-001 Recovery module folder and boundary test"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
epic: "EPIC-001"
status: "SUCCESS"
revision: "v4 (spec gate round 2 remediation of REVIEW-RWB-TE-001-029..032; v3 kept as spec.run2.md)"
prepared: "2026-11-18"
---

# Technical Specification: RWB-TE-001 Recovery module folder and boundary test

| Field | Value |
|---|---|
| Story / epic | `RWB-TE-001` / `EPIC-001` (increment card `aisdlc/docs/increments/INC-002-epic-1-RWB-TE-001.md`). The earlier Jira key `TB0001-1235` is history only (finding 028). |
| Module | P2 Integration (technical enabler); build order 2 of 72 (card) |
| RUN_ID | `INC-002-epic-1-RWB-TE-001` |
| Code repository | This repository (`<repo>`, RUN-BRIEF "Paths"). Backend root package `th.co.scb.ace.demo.recovery`; frontend folder `frontend/src/modules/recovery/`. |
| Source requirement | [S] story file v7, RWB-TE-001 v1 (28 Oct 2026), the canonical version (D-RCV-51) |
| Governing decisions | D-RCV-35 §8.2, D-RCV-36 §3.3 (client decisions, highest precedence); ADR v3 (ADR-002, ADR-010); Decision Log v10 (DL05 option B, DL07, DL36); D-RCV-02, -05, -10, -11, -19, -21, -28 (3), -37..-44, -51, -52; L-RCV-03, L-RCV-14 |
| Supersedes | `_v2-baseline/specify/spec.md` (16 Nov 2026). Its ACE-monorepo evidence (commit `96b0d1c6`, Nx, `DemoApplication`, 13 `Type.OPEN` packages) is **history only** and is not used here. |
| Status | `SUCCESS`. Every source conflict is settled by precedence or a labelled assumption (`assumptions.md`); no blocker gap (`document-gaps.md`). v4 fixes round-2 findings 029–032 (`gate-response.md` Round 2). |

## Source keys

| Key | Document (name, version) and path |
|---|---|
| [S] | Story file v7, RWB-TE-001 v1: `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-001-recovery-module-folder-and-boundary-test-v1.md` |
| [V7 key] | Another story file v7 in the same folder (for example [V7 E1-071] = `rwb-e1-071-temporal-worker-and-sdk-in-the-recovery-module-v1.md`) |
| [D36] | D-RCV-36 Temporal and Drools change register v1 (16 Nov 2026): `requirement/legacy/16-temporal-and-drools-adoption/recovery-workbench-temporal-and-drools-change-register-v1.md` (working copy `aisdlc/docs/decisions/d-rcv-36-temporal-and-drools.md`) |
| [D35] | D-RCV-35 ACE DB alignment change register v1 (15 Nov 2026): `requirement/legacy/15-ace-db-alignment/recovery-workbench-ace-db-alignment-change-register-v1.md` (working copy `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md`) |
| [ADR] | Architecture Decision Records v3: `requirement/legacy/05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md` |
| [API] | API Specification v4: `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| [DL] | Decision Log v10: `requirement/legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| [REG] | Local decisions D-RCV-xx and L-RCV-xx: `aisdlc/docs/decisions/decision-register.md`, `aisdlc/docs/decisions/INC-001-decisions.md` |
| [TS] / [BS] / [FS] | `aisdlc/.github/contexts/testing-standards.md` (CTX-TESTING-RWB-V2, 2.0); `backend-standards.md`; `frontend-standards.md` |
| [SEG] / [IEG] | `aisdlc/.github/rules/specification-execution-gates.md`; `implementation-execution-gates.md` |
| [AUD] | `aisdlc/evidence/phase0-standards-audit.md` (A-01, A-02, A-04, A-09, A-11) |
| [RB] / [README] | `aisdlc/RUN-BRIEF.md`; `README.md` "Decisions taken while setting this up" |
| [CODE] | This repository as read on 17 and 18 Nov 2026 (no git run, no code edited) |
| [BLOG] | `AI-SDLC-BUILD-LOG.md` §1 decisions D-RUN-06..-13 and the orchestrator triage row for RWB-TE-001 (2026-11-17T23:57:10) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` ([SEG]: no prior trace chain for the module map and boundary rules). It is built on the platform baseline, which it extends and does not duplicate ([RB] "What already exists is baseline"; [AUD] A-01, A-02). The previous gate confirmed this classification. |
| UI In Scope | `NO`. No screen, route, component, label or i18n key. |
| Logic In Scope | `YES`. Module map, map loader, module-map rule, BND-1, BND-2, BND-4, BND-5 (map-driven), BND-3 via the existing `ModulithTest`, relocation of the baseline modules into the 19 design modules, coverage tests. |
| API In Scope | `NO`. No endpoint added, removed or changed. Two existing controllers move package; their paths, security and responses are unchanged (SPEC-022). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | Backend main: every class under `recovery.platform`, `recovery.rules`, `recovery.workflow`, `recovery.documents` (relocated, SPEC-022; property binding split, SPEC-023). Backend test: `recovery/architecture/RecoveryBoundaryTest.java` (extended; literal Blob rule replaced; determinism rule retargeted, SPEC-026); `QuartzTimerSchedulerTest`, `DroolsRuleEngineTest`, `PdpaPayloadCodecTest`, `PlatformSmokeWorkflowTest` (move with their classes; FQCN strings only, SPEC-022 (f)). `backend/build.gradle.kts` (JaCoCo verification counters and tooling class directory, SPEC-020). Frontend: one new test file only (SPEC-015). |
| New Nodes Required | `YES`. 19 module packages with `api` / `internal` `package-info.java` (SPEC-001); published sub-packages that receive relocated types, and the non-published implementation sub-packages `casewf.workflow.internal` and `casewf.timers.internal` (SPEC-022); `backend/src/test/resources/architecture/recovery-modules.yaml` (SPEC-002); test-scope `ModuleMapLoader` and rule factory (SPEC-003..-010); backend fixtures and fixture maps (SPEC-011); unit tests that lift relocated classes to the coverage gate (SPEC-024); `frontend/src/modules/recovery/__tests__/importBoundary.test.ts` (SPEC-015, name may change in the plan). |
| Inherited Existing Behavior (kept, must stay green) | `ModulithTest` (`ApplicationModules.of(AceRecoveryApplication.class).verify()` and Documenter); `RecoveryBoundaryTest.workflowImplementationsAreDeterministic` (BS-6.1); `RecoveryBoundaryTest.noRecoveryClassNamesAPublicTable` (BND-6 regex, owned by RWB-E1-069); `RecoveryMigrationLintTest`; JaCoCo tasks `recoveryCoverageReport` / `recoveryCoverageVerification` (`test` is `finalizedBy` the report); `recoveryIntegrationTest` (D-RCV-44); the D-RCV-39 ESLint block in `frontend/eslint.config.js`; Vitest 5.1.0 with `@vitest/coverage-v8` 5.1.0 and 80% thresholds in `frontend/vite.config.ts`; `npm run check`; CI jobs `backend-unit`, `frontend-check`, `backend-recovery-it` in `.gitlab-ci.yml` [CODE]. |
| Frontend Changes Required | `YES`. Test only: the AC6 fixture test (SPEC-015). No runtime code, no config edit, no new dependency. |
| Backend Changes Required | `YES`. Package relocation without behaviour change, module skeleton, test-scope boundary tooling, coverage tests, one Gradle edit. |

Not changed: `.gitlab-ci.yml` (D-RCV-05), `scripts/dev.ps1`, `application*.yaml` property keys, `frontend/eslint.config.js`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/package.json`, any migration, any endpoint contract.

## Requirement-to-SPEC Logic Coverage

Acceptance for this story is AC1–AC7 and BR1–BR6 of [S] §7–§8. The v7 story file is canonical (D-RCV-51), so the earlier premise that the story has no ACs (D-RCV-16) no longer applies (gap DG-01, resolved by D-RCV-51).

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| AC1 / X1 / TC-TE-001-01 | `recovery.casewf.internal.SampleService` importing `collection.internal.CollectorRepository` fails; the log names BND-1, `SampleService` and `CollectorRepository`. | SPEC-005, -010, -011 | DIRECT | Fixture names are the AC's class names under a fixture root (SPEC-011). | COVERED |
| AC2 / TC-TE-001-02 | `SampleService` calling an interface in `common.api` passes. | SPEC-006, -011 | DIRECT | Passing fixture. | COVERED |
| AC3 / X2 / TC-TE-001-03 | `recovery.integration.internal` class importing `recovery.decision.internal.DecisionLogRepository` fails with BND-3; importing published `recovery.decision.writer.DecisionLogWriter` passes. | SPEC-007, -011 | DIRECT | **Accepted deviation:** the failure text is Spring Modulith's own, not "boundary rule BND-3" (D-RCV-42, recovery tech lead 2026-11-09). | COVERED (deviation recorded) |
| AC4 / X3 / TC-TE-001-04 | `recovery.integration.internal` class using entity `recovery.casewf.internal.RecoveryCaseEntity` fails with BND-4. | SPEC-008, -011 | DIRECT | D-RCV-38. | COVERED |
| AC5 / X4 / TC-TE-001-05 | `java.net.http.HttpClient` in `recovery.casewf.internal` fails BND-5; in `recovery.integration.adapter` passes. | SPEC-009, -011 | DIRECT | D-RCV-41 library list. | COVERED |
| AC6 / X5 / TC-TE-001-06 | A component in `src/modules/recovery/caselist` importing the collection `WorkList` fails the frontend rule. | SPEC-014, -015 | DIRECT | **Accepted deviation:** rule name is `no-restricted-imports` (D-RCV-39 allow-list), not `no-collection-import`; the import is written `@/modules/collection/worklist/WorkList` or a `../` path because this repository has no `src/modules/collection` and uses the `@/` alias (D-RCV-10, D-RCV-39). Both forms are in the rejected set. | COVERED (deviation recorded) |
| AC7 / X6 / TC-TE-001-07 | A new package `recovery.vendorx` not in the map fails with `package recovery.vendorx is not in the module map`. | SPEC-003, -004, -010 | DIRECT | `{package}` prints the fully qualified name; the test asserts the text ends with `recovery.vendorx is not in the module map`. | COVERED |
| X7 / TC-TE-001-08 / MSG-P4-002 / Flow 5 / §13 step 6 | `RecoveryAccessGuard`, 403 MSG-P4-002 access test. | SPEC-016 | — | **Moved out of scope** to RWB-E1-022 (D-RCV-52). Destination: [V7 E1-022] X1 and AC2 carry the 403 MSG-P4-002 refusal; that story does not yet name `RecoveryAccessGuard` or TC-TE-001-08 (gap DG-02; `shared-updates.md` SU-05). | MOVED_OUT_OF_SCOPE |
| BR1 | BND-1: collection only through its published packages. | SPEC-005 | DIRECT | `allowEmptyShould(true)` (D-RCV-19); root `th.co.scb.ace.demo.collection`, published `[api]` (D-RCV-41). | COVERED |
| BR2 | BND-2: common only through its published packages. | SPEC-006 | DIRECT | Root `th.co.scb.ace.demo.common`, published `[api]` ([S] §3; DL05). | COVERED |
| BR3 | BND-3: another recovery module only through a published package or an application event. | SPEC-004 (d)–(f), -007 | DIRECT | Existing `ModulithTest` (D-RCV-11, D-RCV-42). | COVERED |
| BR4 | BND-4: entities and repositories used only inside their module. | SPEC-008 | DIRECT | D-RCV-38. | COVERED |
| BR5 | BND-5: client libraries only in map-allowed client packages; no recovery class calls a system of record. | SPEC-009, -022 | DIRECT | REQ-DRI-006; [ADR] ADR-010 (ADR-005 is superseded, gap DG-03). Initial `clientPackages`: P2 `[adapter]`, P5 `[storage]`, P10 `[client]`. Replaces the literal baseline Blob test. | COVERED |
| BR6 | Names, packages and published packages come from the map, not the test. | SPEC-002, -003, -004, -026 | DIRECT | No recovery package literal in the rule code. | COVERED |
| Flow 1 / §13 step 1 | 19 module packages with `api` and `internal`; frontend folder. | SPEC-001, -013, -022 | DIRECT | Frontend folder exists (inherited). | COVERED |
| Flow 2 / §13 step 2 | Module map and `ModuleMapLoader` with a test for AC7. | SPEC-002, -003 | DIRECT | D-RCV-37 location. | COVERED |
| Flow 3, 7, 8 / §13 steps 3–4 / §14 | Rules BND-1..5 from the map; one breaking fixture per rule; passing common-api fixture; failure text; fix through `api` or event. | SPEC-004..-011 | DIRECT | §14 text for ArchUnit rules. | COVERED |
| Flow 4 / §13 step 5 | Frontend boundary rule and a breaking fixture. | SPEC-014, -015 | INHERITED_EXISTING_BEHAVIOR (rule) / DIRECT (fixture test) | Rule exists (D-RCV-39); this story adds the fixture test. | COVERED |
| Flow 6 / §13 step 7 | Checks run on every merge request and on the default branch; "confirm a failing fixture blocks a merge". | SPEC-012 | INHERITED_EXISTING_BEHAVIOR (pipeline jobs) / DIRECT (local merge gate, T-TE001-13) | CI `backend-unit` runs `test`; `frontend-check` runs `npm run check`. No pipeline change (D-RCV-05). Locally, T-TE001-13 proves that a real violation makes `./scripts/dev.ps1 test` exit non-zero, and the orchestrator merges into `develop-recovery` only on a zero exit ([BLOG] triage; D-RUN-06). Host-side merge blocking (GitLab) is human-verification item HV-01, not tested (finding 032). | COVERED (HV-01 open for the host) |
| §17 Guardrails | No business value, no personal data, fixtures in `src/test` only. | SPEC-011, -019 | DIRECT | Class and package names only. | COVERED |
| §19 Out of scope | TE-002, TE-003, common/collection internals, E1-007. | SPEC-016 | DIRECT | Not built. | COVERED |
| Card / AUD A-01 | Map the existing technical slices to P/S modules. | SPEC-022, -023 | DIRECT | Finding 019. | COVERED |

## User story intent interpretation

As a squad member (RW-TRIBE), I want the recovery module folder and packages with a build-time boundary test, so that no module calls the inside of another module and no recovery code calls a system of record directly ([S] §1).

In this repository the recovery root and a four-module technical skeleton (`platform`, `rules`, `workflow`, `documents`) already exist [CODE]. The story therefore (1) creates the 19 design modules of [S] §13, (2) moves the existing code into the homes that D-RCV-36 §3.3 and the v7 stories give, (3) adds the module map, its loader and the map-driven rules, and (4) proves the existing frontend rule with the AC6 fixture test. It adds no runtime behaviour. A violation is a failed merge request; the measure is zero violations merged ([S] §2).

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Every merge request and default-branch build: CI `backend-unit` (`./gradlew test recoveryCoverageReport`) and `frontend-check` (`npm ci`, `npm run check`, `npm run build`) [CODE `.gitlab-ci.yml`]. Locally `./scripts/dev.ps1 test` [RB]. |
| Preconditions | DL05 option B ([S] §3); recovery root and baseline modules present [CODE]; RWB-E1-044 (build order 1) may have changed `RecoveryFlywayConfig` first; SPEC-022 (g) covers it. |
| Input | Compiled main classes under `th.co.scb.ace.demo.recovery`; the module map; frontend files under `frontend/src/modules/recovery/`. |
| Output | Pass, or a failed test or lint naming the rule, the class or file, and the dependency. |
| Feature flag | None; a build check has no runtime path ([S] §13). |

## Field-level behaviour matrix

No business field is read or written ([S] §11). The fields are those of the module map, the only data artefact (`contracts/backend-apis.json` `CON-RWB-TE-001-001`).

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| Module map | `rootPackage` | `th.co.scb.ace.demo.recovery` (D-RCV-02) | Merge request; code-owner approval once RWB-TE-002 is in place (D-RCV-21) | Exactly one; valid Java package name. |
| `modules[]` | `code` | [S] §13: P1..P10, S1..S9 | As above | Required; unique; `^(P([1-9]\|10)\|S[1-9])$`. |
| `modules[]` | `name` | [S] §13: `dataengine`, `integration`, `casewf`, `access`, `dochub`, `comms`, `decision`, `payments`, `reporting`, `agent`, `valuation`, `treatment`, `guarantee`, `litigation`, `asset`, `debtsale`, `writeoff`, `deviation`, `partner` | As above | Required; unique; `^[a-z][a-z0-9]*$`; module package = `rootPackage.name`. |
| `modules[]` | `published` | Initial: `casewf [api, rules, timers, workflow]` (D36 §3.3); `integration [api, flags.api]` ([V7 E1-047] §12); every other module `[api]` ([S] §13) | Later stories add their own entry, with its `@NamedInterface`, in their own merge request. Known: `casewf.allocation` (RWB-E1-020) and `decision.writer` (RWB-E1-027) ([S] §13); `casewf` `config.api` (RWB-E1-042, [V7 E1-042] §13; holds `ParameterLoadHandler`, D-RUN-10); `casewf` `refdata.api` (RWB-E1-043, [V7 E1-043] §13; holds the table-code handler registry, D-RUN-11); `integration` `generated.web`, `generated.model` (RWB-TE-003, L-RCV-14). Multi-segment entries fit the pattern, so the map needs no schema change for them. | Non-empty; relative sub-package names `^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$`; unique per module; never `internal` or under it. Each entry is published alone: its sub-packages are not published unless listed (`propagate = false`, SPEC-004 (d)). |
| `modules[]` | `clientPackages` | Initial: `integration [adapter]` ([S] BR5; RWB-E1-007); `dochub [storage]` ([V7 TE-012] §13; finding 022); `agent [client]` ([S] BR5; RWB-TE-013); others `[]` | Code-owner approval; later stories add their own (D-RCV-41) | Relative sub-package names; may name a package that does not exist yet (a permission). |
| `external[]` | `name`, `rootPackage`, `published` | `common`: `th.co.scb.ace.demo.common`, `[api]` ([S] §3; DL05); `collection`: `th.co.scb.ace.demo.collection`, `[api]` (D-RCV-41) | ACE team names real values (DL05); the map changes, not the rule | Both entries required. |
| Module map | `clientLibraries` | The 16 entries of D-RCV-41: `java.net.http`, `java.net.HttpURLConnection`, `java.net.Socket`, `java.net.URL`, `org.springframework.web.client`, `org.springframework.web.reactive.function.client`, `org.apache.hc`, `org.apache.http`, `okhttp3`, `com.jcraft.jsch`, `org.apache.sshd`, `net.schmizz.sshj`, `org.apache.commons.net`, `com.azure.storage`, `org.springframework.kafka`, `org.apache.kafka` | Code-owner approval | Non-empty; unique; name-boundary match (SPEC-009). |
| Module map | `sourceViews` (reserved) | Not written by this story. Owned by RWB-E1-069 ([V7 E1-069] §13; D35 §8.2) | E1-069 | Optional top-level key. The TE-001 loader accepts it without validating it and keeps it in the model untouched (SPEC-003). Any other unknown key fails. |

## Status-transition matrix

No case status changes ([S] §9). The only state is the result of a build.

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Build passed | Commit adds a dependency or a package | A BND rule, the module-map rule or `verify()` is broken | Build failed | Failure text names rule, class and dependency (SPEC-010); `./scripts/dev.ps1 test` exits non-zero (T-TE001-13), and the orchestrator does not merge into `develop-recovery` (SPEC-012 (b)). On the GitLab host, blocking by the failing job depends on the project's merge setting: HV-01, not verified here. |
| Build failed | Commit routes the call through a published package or an event, or adds the package to the map | No rule broken | Build passed | Merge subject to review (code owners once RWB-TE-002 is in place). |
| Build passed | Commit adds a forbidden import under `frontend/src/modules/recovery/` | ESLint rule broken | Build failed | ESLint names the file, line and import. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / evidence | SPEC |
|---|---|---|---|---|
| X1 | Recovery class imports a collection non-published class | `RecoveryBoundaryTest` fails | `Rule BND-1 broken: …` | SPEC-005, -010 |
| X2 | Recovery module imports another module's non-published class | `ModulithTest` fails | Spring Modulith's text naming both modules and types (accepted deviation, D-RCV-42) | SPEC-007 |
| X3 | Class uses another module's entity or repository | Fails | `Rule BND-4 broken: …` | SPEC-008, -010 |
| X4 | Class outside an allowed client package uses a listed client library | Fails | `Rule BND-5 broken: …` | SPEC-009, -010 |
| X5 | Recovery file imports outside the D-RCV-39 allow-list | `npm run lint` fails | ESLint `no-restricted-imports` with the D-RCV-39 message (accepted deviation from `no-collection-import`) | SPEC-014, -015 |
| X6 | Package under the root not in the map; type in the root package; map and annotations disagree | Fails before the BND rules | `package {package} is not in the module map` and the SPEC-004 texts | SPEC-004, -010 |
| X-B2 | Recovery class depends on a non-published common class (derived from BR2; not a story X ID) | Fails | `Rule BND-2 broken: …` | SPEC-006, -010 |
| X-B7 | Map missing, unreadable or invalid (derived from §13 step 2) | Fails | Loader error naming file and field | SPEC-003 |
| X7 | Role without the right calls a recovery endpoint | Moved out of scope (D-RCV-52; RWB-E1-022 X1, AC2) | — | SPEC-016 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Endpoints added or changed | None. `TemporalAdminController` (`/api/recovery/v1/admin/...`) and `PlatformInfoController` (`/api/recovery/v1/platform/info`) change Java package only; paths, method security, request and response bodies are unchanged (SPEC-022 (e)). `/admin/workflows/smoke` keeps `x-module: P3` ([API]); `/platform/info` and `/admin/temporal/health` stay local operational endpoints ([README] item 6). |
| Backend-only contract | Module map schema and rule set: `contracts/backend-apis.json` (`CON-RWB-TE-001-001`, `-002`). |
| Frontend contract | Lint rule (inherited) and its fixture test: `contracts/frontend-integrations.json`. |
| Backward compatibility | Property keys unchanged (SPEC-023). Temporal workflow type names and task queues unchanged. Drools decision-table class names of `RuleInput` / `RuleOutcome` (in the `Import` and `Variables` rows) change with their package; no rule package is stored in this repository yet [CODE], so only the test workbook changes (SPEC-022 (f)). |
| Versioning | None. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES (test only) | REQUIRED | 80% lines, statements, branches and functions on `src/modules/recovery/**` excluding `__tests__` and `i18n`, by `@vitest/coverage-v8` with the thresholds already in `frontend/vite.config.ts` (inherited; D-RCV-40; [TS] §1). Measured on the existing recovery frontend code, which this story does not change. Baseline as printed in `aisdlc/evidence/baseline-test.log`: Statements 91.89% (34/37), Branches 88.09% (37/42), Functions 82.35% (14/17), Lines 91.66% (33/36). Expected result: `PASS`, with the Builder's own run recorded as printed. Coverage Type for runtime files: `INHERITED_EXISTING_BEHAVIOR`; for the import rule: `DIRECT` (proved by T-TE001-07, not by coverage). | SPEC-013, -014, -015, -020 | The only new file is a test under `__tests__` (excluded from coverage by the existing config). No fixture file on disk, so no ignore, tsconfig or coverage-config edit (SPEC-015). | AC6 import and every other rejected form report `no-restricted-imports`; every allowed form reports none; `npm run check` green. |
| Backend | YES | REQUIRED | 80% LINE, INSTRUCTION (statements), BRANCH and METHOD (functions), bundle level, by JaCoCo `recoveryCoverageVerification` over **all** main classes under `th/co/scb/ace/demo/recovery/**` plus the test-scope boundary tooling package (`ModuleMapLoader`, rule factory). Excluded only: test classes, `RecoveryBoundaryTest`, fixtures. No main class is excluded ([IEG]; finding 020). Baseline from `backend/build/reports/jacoco/recoveryCoverageReport.xml`: LINE 133/415 (32%), BRANCH 25/92 (27%), INSTRUCTION 686/2174, METHOD 41/135. Expected: `FAIL` at baseline; `PASS` once SPEC-024 tests land, before the code gate. Coverage Type: `DIRECT` for all relocated classes and tooling. | SPEC-001..-012, -017, -018, -020, -022..-024, -026 | This story relocates every baseline class, so every class is changed code and in scope ([TS] §6 changed code first; [BS] BS-7.2; [IEG] untested files included, no added exclusions). The story raises their coverage itself through SPEC-024. | Each BND rule fails on its breaking fixture and passes on its passing fixture; loader error paths; `RecoveryBoundaryTest` and `ModulithTest` pass on real main classes; `./gradlew test recoveryCoverageVerification` passes. |

## Detailed specification (SPEC-*)

SPEC-001..-020 keep their v2 IDs; changed text is re-based on this repository. SPEC-021 (BND-6) is withdrawn (finding 023). SPEC-022..-026 are new.

| SPEC ID | Specification | Traces to |
|---|---|---|
| SPEC-RWB-TE-001-001 | **Module skeleton.** (a) Keep `recovery/package-info.java` (`@ApplicationModule`, `displayName` "Recovery") with no other type in the root package. (b) For each of the 19 map modules: `recovery.<name>/package-info.java` with `@ApplicationModule`; `recovery.<name>.api/package-info.java` with `@NamedInterface(name = "api", propagate = false)`; `recovery.<name>.internal/package-info.java` with no annotation. (c) Every other published package of the initial map (`casewf.rules`, `casewf.timers`, `casewf.workflow`, `integration.flags.api`) gets `package-info.java` with `@NamedInterface(name = "<relative package>", propagate = false)`. The implementation sub-packages `casewf.workflow.internal` and `casewf.timers.internal` carry no `@NamedInterface` (SPEC-022 (c)). (d) The four baseline module packages `platform`, `rules`, `workflow`, `documents`, with their `package-info.java` files, are removed once empty (SPEC-022). (e) No new bean, controller, entity or configuration; only relocated classes and the property split (SPEC-022, -023). | Flow 1; [S] §13 step 1; D-RCV-02; [BS] BS-1.1, BS-1.2 |
| SPEC-RWB-TE-001-002 | **Module map** at `backend/src/test/resources/architecture/recovery-modules.yaml` (D-RCV-37; the folder exists and is empty, [AUD] A-02). Fields and initial values per the Field-level behaviour matrix. Test resource only; not packaged in the jar. | BR6; Flow 2; D-RCV-37 |
| SPEC-RWB-TE-001-003 | **`ModuleMapLoader`** (test scope) reads the map with SnakeYAML (on the classpath through Spring Boot; the plan confirms with `./gradlew dependencies --configuration testRuntimeClasspath`) into an immutable model. It fails, naming file and field path, when: the file is missing or not valid YAML; a required field is missing or empty; a `code` or `name` repeats; a value breaks its pattern; a published entry is `internal` or under it; a top-level or nested key is unknown. Exception: the optional top-level `sourceViews` key is accepted unvalidated and carried as an opaque value for RWB-E1-069 (finding 023; [V7 E1-069] §13; E1-069 spec ASM-006). No package literal in the loader. | BR6; [S] §13 step 2; X-B7 |
| SPEC-RWB-TE-001-004 | **Module-map rule** (first in `RecoveryBoundaryTest`, on main classes): (a) every package directly under `rootPackage` that holds a class, directly or in a sub-package, is a map module, else `package {package} is not in the module map`; (b) every map module package exists (has `package-info`); (c) no type other than `package-info` sits in the root package; (d) every package with `@NamedInterface` under a module is in that module's `published`, and every listed published package that exists carries `@NamedInterface`, else a text naming the package and the side that disagrees; every `@NamedInterface` under the root declares `propagate = false`, else `@NamedInterface on {package} must declare propagate = false; list each published sub-package in the module map`; (e) no public type directly in a module base package `recovery.<name>`, else `public type {class} in module base package {package}; move it to a published package or internal`; (f) no type-level `@NamedInterface` under the root, else `type-level @NamedInterface on {class}; declare published packages in package-info and the module map`. Sub-packages belong to their module. Spring Modulith 2.1.1 `@NamedInterface` has `propagate = true` by default, which would publish every sub-package of a published package without a map entry. Rule (d) therefore requires `propagate = false`, so the published surface is exactly the map's list (BR6) and an implementation sub-package such as `casewf.workflow.internal` stays internal to its module (SPEC-022 (c); finding 030; ASM-09). (g) **Known downstream conflicts** (gap DG-04; no code change here): [V7 E1-072] §13 and [V7 E1-073] §13 `recovery.accessadmin.rulepackages`; [V7 E1-014] §13 `recovery.decisionlog.api`; [V7 E1-065] §13 and [V7 TE-004] §13 `recovery.tools.*`; [V7 TE-003] §13 `recovery.generated.*`. None is a map module, so rule (a) would fail them. Under D-RCV-02 (19 nested modules) the owning story moves the package into a map module (for example P4 `access.rulepackages`, P7 `decision.log`; generated code to `integration.generated.web` / `integration.generated.model` per L-RCV-14, which rejects a 20th module) or changes the map with code-owner approval. `shared-updates.md` SU-09 tells each owner. | BR3; BR6; X6; D-RCV-02, -11, -42; L-RCV-14; AC7 |
| SPEC-RWB-TE-001-005 | **BND-1 (collection):** no class under `rootPackage` depends on a class under `external.collection.rootPackage` unless it sits in one of its `published` packages. ArchUnit, `allowEmptyShould(true)`. | BR1; AC1; D-RCV-19, -41; DL05 |
| SPEC-RWB-TE-001-006 | **BND-2 (common):** the same for `external.common`. | BR2; AC2; D-RCV-19; [S] §3 |
| SPEC-RWB-TE-001-007 | **BND-3 (recovery to recovery):** enforced by the existing `ModulithTest` unchanged, using the nested-module and `@NamedInterface` declarations of SPEC-001/-022; SPEC-004 (d)–(f) keep them equal to the map (BR6). Modulith also fails dependency cycles between modules and counts event types as type dependencies (D-RCV-11). Failure text is Modulith's (D-RCV-42; AC3 deviation). TC-TE-001-03 runs `ApplicationModules.of(<fixture root>, <import option that includes test classes>).verify()` on a fixture module set; if Modulith 2.1.1 cannot import test-scope fixtures, the plan stops and reports before building. | BR3; AC3; D-RCV-11, -42; [BS] BS-1.3 |
| SPEC-RWB-TE-001-008 | **BND-4 (entities and repositories):** an entity is a class annotated `@jakarta.persistence.Entity`; a repository is a subtype of `org.springframework.data.repository.Repository`. A class under `rootPackage` may depend on one only if both are in the same recovery module; every other entity and repository is forbidden (D-RCV-38). Direct SQL against another module's table is not detectable here and stays a review item ([BS] BS-2.4). Today's main code has no entity or repository [CODE], so the rule passes on it. | BR4; AC4; D-RCV-38 |
| SPEC-RWB-TE-001-009 | **BND-5 (client libraries):** no class under `rootPackage` depends on a class matching a `clientLibraries` entry unless it sits in, or under, a `clientPackages` package of its own module. Match on a name boundary: equals the entry, or starts with `entry.` or `entry$` (so `java.net.URL` does not match `java.net.URLEncoder`; `java.net.URI` and `java.net.InetAddress` do not match any entry). Initial allowed packages: `integration.adapter`, `dochub.storage`, `agent.client`. This map-driven rule **replaces** the literal baseline test `blobClientOnlyInDocumentsModule` (BR6; finding 022). After SPEC-022 the only listed-library user in main code is `BlobDocumentStore` (`com.azure.storage`) in `dochub.storage` [CODE], so the rule passes. | BR5; AC5; REQ-DRI-006; [ADR] ADR-010; D-RCV-41 |
| SPEC-RWB-TE-001-010 | **Failure text** (build log, not the message standard, [S] §14): ArchUnit rules print `Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event.`; `{module}` is the target's map name (BND-1, -2, -4) or the allowed client package (BND-5). One line per violation; all violations of a rule in one run. Map texts per SPEC-004. BND-3 shows Modulith's text. Class and package names only. | [S] §14; Flow 7; X1–X6 |
| SPEC-RWB-TE-001-011 | **Backend fixtures** (test scope only): one breaking and one passing fixture per rule plus the common-`api` passing fixture, using the AC class names (`SampleService`, `CollectorRepository`, `DecisionLogRepository`, `DecisionLogWriter`, `RecoveryCaseEntity`, `HttpClient` user, `vendorx`). Fixture root is a package outside `th.co.scb.ace.demo` (plan names it), mirroring `recovery.<module>...`, `collection.internal`, `common.api`, with fixture maps under `backend/src/test/resources/architecture/fixtures/`. Main-class imports use `DO_NOT_INCLUDE_TESTS`, so neither `RecoveryBoundaryTest` on main classes nor `ModulithTest` sees fixtures. | [S] §13 steps 3–4; §17; AC1–AC5, AC7 |
| SPEC-RWB-TE-001-012 | **Execution and merge gate (§13 step 7).** (a) Plain JUnit 5, untagged, in the `test` task; no Docker, Spring context or database for boundary tests. No change to `.gitlab-ci.yml` (D-RCV-05): CI `backend-unit` already runs `test`, publishes the JUnit report, and `frontend-check` runs `npm run check`. Same commit, same result. (b) **Local merge gate.** `./scripts/dev.ps1 test` runs `gradlew test` and then `npm run check` and throws when either exits non-zero ([CODE] `scripts/dev.ps1`: the `test` command and the exit-code checks in `Invoke-Gradle` / `Invoke-Npm`), so a boundary violation makes it exit non-zero. The orchestrator merges a story branch into `develop-recovery` only when `./scripts/dev.ps1 test` exits 0 on that branch ([BLOG] RWB-TE-001 triage; D-RUN-06: the orchestrator alone merges). T-TE001-13 proves (b) with a real violation in main code and in a recovery frontend file, because the fixtures run in expect-failure mode and always pass. (c) **Host-side merge blocking** (GitLab "Pipelines must succeed" on the merge request) cannot be checked here: no GitLab MCP (RUN-BRIEF rule 5). It is human-verification item HV-01 and is never reported as tested. | Flow 6; [S] §12, §13 step 7, "Done when"; D-RCV-05; [TS] §1; finding 032 |
| SPEC-RWB-TE-001-013 | **Frontend folder:** `frontend/src/modules/recovery/` exists with runtime code [CODE]. Inherited; no change. | Flow 1; D-RCV-10 |
| SPEC-RWB-TE-001-014 | **Frontend import rule:** the D-RCV-39 block (`recoveryImportRule`) in `frontend/eslint.config.js` already applies to `src/modules/recovery/**/*.{ts,tsx}`: `../` imports forbidden; `@/` imports allowed only for `components/ui/**`, `lib/utils`, `utils/*` not starting `cfsc`, `contexts/ApiClientContext`, `api/schema`, `modules/recovery/**`. Inherited; no change. | Flow 4; D-RCV-39; [FS] FS-1.2 |
| SPEC-RWB-TE-001-015 | **Frontend fixture test (AC6, TC-TE-001-06).** One Vitest test, `frontend/src/modules/recovery/__tests__/importBoundary.test.ts` (plan may rename), uses the ESLint Node API (`new ESLint({ cwd: <frontend root> })`, which loads the real `eslint.config.js`) and `lintText(source, { filePath: "src/modules/recovery/caselist/<File>.tsx" })` on in-memory fixture sources, so the recovery block applies. The fixtures are string constants in the test, committed with it; no fixture file on disk, so no ESLint ignore, tsconfig exclude or coverage exclude is needed (deviation from review plan input 7, ASM-07). Rejected set (each yields a `no-restricted-imports` error): `@/modules/collection/worklist/WorkList` (AC6), `../../collection/worklist/WorkList` (AC6 relative form), `@/hooks/cfsc/x`, `@/api/tdr/config`, `@/pages/x`, `@/utils/cfscCaseList`, `@/modules/other/x`, `../x`. Allowed set (no error): `@/components/ui/button`, `@/lib/utils`, `@/utils/date`, `@/contexts/ApiClientContext`, `@/api/schema`, `@/modules/recovery/casewf/x`, `./sibling`. Runs in the existing `npm run check` (`coverage` script); no new dependency (ESLint 9.39.5 ships its types). | [S] §13 step 5; AC6; D-RCV-06, -39, -40 |
| SPEC-RWB-TE-001-016 | **Scope exclusions:** `RecoveryAccessGuard`, its wiring, the test-only Case record R endpoint, TC-TE-001-08 and MSG-P4-002 (to RWB-E1-022, D-RCV-52; [V7 E1-022] X1/AC2); pipeline stages (D-RCV-05); code owners (RWB-TE-002); OpenAPI types and contract tests (RWB-TE-003); common/collection internals (DL05 option A); adapter pattern (RWB-E1-007); agent client (RWB-TE-013); BND-6 and `sourceViews` (RWB-E1-069, D35 §8.2); `PlatformInfoController`'s BND-6 disposition (RWB-E1-069); the `RuleEngine`→`RuleEvaluator` and `TimerScheduler` signature alignment with D36 §3.3 (RWB-E1-072, RWB-E1-028). | D-RCV-52, -05; [S] §19; D35 §8.2 |
| SPEC-RWB-TE-001-017 | **Dependency and shared-file footprint:** no new dependency (ArchUnit 1.5.1 is an explicit `testImplementation`; Modulith 2.1.1; temporal-testing, webmvc-test and security-test are present [CODE `build.gradle.kts`]). Edited shared file: `backend/build.gradle.kts` only (SPEC-020). Frontend: one new test file. | [BS] BS-1.4; D-RCV-05 |
| SPEC-RWB-TE-001-018 | **Regression:** `./gradlew test` (all unit tests, `ModulithTest`, `RecoveryBoundaryTest`, `RecoveryMigrationLintTest`), `./gradlew recoveryIntegrationTest` (Docker; required because `RecoveryFlywayConfig` moves, D-RCV-44), `./gradlew e2eTest` against the local stack (the moved controllers answer as before), and `npm run check` all pass. | [BS] BS-1.4; [TS] §1; D-RCV-44 |
| SPEC-RWB-TE-001-019 | **Guardrails:** no business value, route or personal data in code, map, fixtures or failure text; synthetic class names only; map and rule changes by merge request with code-owner approval once RWB-TE-002 lands (D-RCV-21). | [S] §17; D-RCV-21 |
| SPEC-RWB-TE-001-020 | **Native coverage.** Backend: edit the existing tasks in `backend/build.gradle.kts`. (a) `recoveryCoverageVerification` gets four limits at 0.80: LINE, INSTRUCTION, BRANCH, METHOD (today LINE and BRANCH only). (b) Both tasks add the test-output class directory of the tooling package (`ModuleMapLoader`, rule factory) to `classDirectories`, excluding test classes, `RecoveryBoundaryTest` and fixtures; the main `recovery/**` tree stays whole. (c) Execution data stays the `test` task (unit coverage only; integration coverage is not substituted, [IEG]). (d) Tasks stay outside `check` (D-RCV-28 (3), D-RCV-40). (e) The Builder runs `./gradlew test recoveryCoverageVerification` and saves the XML/HTML report as evidence. CI runs only the report today; wiring the verification into CI is [AUD] A-09, owned by RWB-TE-003/RWB-TE-011, and is not done here (D-RCV-05; SU-10). Frontend: inherited config, no change (Unit Test Applicability). | D-RCV-28 (3), -40; [TS] §1, §6; [BS] BS-7.2; [IEG] |
| SPEC-RWB-TE-001-021 | **Withdrawn.** BND-6 belongs to RWB-E1-069 (D35 §8.2; [V7 E1-069] §4 step 5, BR8, AC8, §13). The baseline regex test `noRecoveryClassNamesAPublicTable` stays unchanged and green (SPEC-026); the map keeps `sourceViews` open (SPEC-003). | Finding 023 |
| SPEC-RWB-TE-001-022 | **Relocation of the baseline modules (finding 019, [AUD] A-01).** (a) Every class moves as in the Relocation table below; the four baseline module packages cease to exist. (b) Signatures, annotations, bean names, conditions, endpoint paths and behaviour are unchanged; only `package` and `import` lines change, plus the property split of SPEC-023. (c) **Published surface and visibility (finding 030).** Three types are public today and would land in published packages: `PdpaPayloadCodec` (`public final class`), `PlatformSmokeWorkflow` (`public interface`, with its nested `Impl`, `Activities` and `SmokeResult` implicitly public) and `QuartzTimerScheduler.TimerDueJob` (`public static class`). Under BND-3 (D-RCV-11) every public type in a published package is callable from any module, while D36 §3.3 publishes only `TimerScheduler` from `casewf.timers` and `WorkflowGateway` from `casewf.workflow` ("no other new interfaces"), and [V7 E1-071] says the gateway never exposes a Temporal type. Resolution, by the BND-3 rule: Temporal and Quartz implementation code moves out of the published packages into the non-published sub-packages `casewf.workflow.internal` and `casewf.timers.internal`, and every published package declares `propagate = false` (SPEC-001, SPEC-004 (d)), so those sub-packages are not published. Sub-packages keep the code inside `recovery.casewf.workflow..` and `recovery.casewf.timers..`, as [V7 E1-071] BR1 and [V7 E1-028] X10 require. `PlatformSmokeWorkflow` and `TimerDueJob` keep their public visibility, because `casewf.admin.TemporalAdminController` uses the workflow interface from another package, and Temporal and Quartz create these types reflectively; moving them is enough to take them off the published surface. `PdpaPayloadCodec` becomes package-private as well (class and constructor), because only `TemporalConfig` and the tests in its own package use it [CODE]. `TemporalProperties` becomes **public** in the non-published `casewf.workflow.internal`: `TemporalAdminController` reads it from `casewf.admin`, and a package-private record would not compile there (defect found in round 2 while fixing 030). A public type in a non-published package is visible inside P3 only; Modulith rejects its use from another module. Every other type keeps its visibility. After the move the public types in published packages are exactly those listed in SPEC-025. (d) Cross-module dependencies after the move: `casewf.rules` → `integration.flags.api`; `casewf.admin` → `access.api`; no other. No cycle. Consequence for later stories: P3 depends on P2 and P4, so neither `integration` nor `access` may depend on `casewf`, because `ModulithTest` rejects the cycle (D-RCV-11). `shared-updates.md` SU-08 tells RWB-E1-042 and RWB-E1-043. (e) Runtime checks for the plan: component scan under `AceRecoveryApplication` (root `th.co.scb.ace.demo`) still finds every bean; `@RestControllerAdvice(basePackages = "th.co.scb.ace.demo.recovery")` unchanged; `@ConfigurationProperties` prefixes unchanged; Temporal workflow type `PlatformSmokeWorkflow` (simple name) and queue `rwb-platform` unchanged; Quartz job class name changes (in-memory store locally, [RB]; ASM-06). (f) Tests move with their classes into the matching test packages (`QuartzTimerSchedulerTest` → `casewf.timers.internal`; `DroolsRuleEngineTest` → `casewf.rules`; `PdpaPayloadCodecTest`, `PlatformSmokeWorkflowTest` → `casewf.workflow.internal`). Assertions are unchanged. What changes is the `package` and `import` lines and **every fully qualified class-name string** in the test workbook of `DroolsRuleEngineTest`: the `Import` row (today line 97: `th.co.scb.ace.demo.recovery.rules.api.RuleInput, th.co.scb.ace.demo.recovery.rules.api.RuleOutcome`) and the `Variables` row (today line 98: `th.co.scb.ace.demo.recovery.rules.api.RuleOutcome outcome`) both become `th.co.scb.ace.demo.recovery.casewf.rules.*` (`…casewf.rules.RuleInput`, `…casewf.rules.RuleOutcome`, and `…casewf.rules.RuleOutcome outcome`) (finding 031). This is a rename only and changes no expectation, so no test is weakened. Check: after the move, a search of `backend/src` for a string literal containing `th.co.scb.ace.demo.recovery.` followed by `platform`, `rules`, `workflow` or `documents` finds nothing. On 18 Nov 2026 the only such literals are these two workbook rows; the root string `"th.co.scb.ace.demo.recovery"` in `ApiExceptionHandler` and `RecoveryBoundaryTest` stays (T-TE001-06). (g) A class added under the four baseline packages by an earlier merged story (for example RWB-E1-044) moves by the same table; a class the table does not cover goes to its own v7 story §13 home, or the plan stops. (h) `.gitlab-ci.yml` `backend-recovery-it` matches `**/RecoveryFlywayConfig.java`, so the move triggers `recoveryIntegrationTest` (D-RCV-44). | D36 §3.3; [V7 E1-028] §3, §12; [V7 E1-044] §13; [V7 E1-047] §12–§13; [V7 E1-071] §13, BR1; [V7 E1-072] §13; [V7 TE-012] §13; [API]; ASM-01..-03 |
| SPEC-RWB-TE-001-023 | **Property binding split.** `platform.internal.RecoveryProperties` (prefix `rwb`; fields `environment`, `schema`, `p3`, `flyway`, `security`) is read by four classes that land in three modules. It is replaced by package-private records in each consuming module, binding the same keys: `integration.flags` (`rwb.p3.temporal`, `rwb.p3.drools`) for the `RecoveryFlags` bean; `integration.internal` (`rwb.environment`, `rwb.schema`) for `PlatformInfoController`; `casewf.migration` (`rwb.schema`, `rwb.flyway.*`) for `RecoveryFlywayConfig`; `access.internal` (`rwb.security.*`) for `SecurityConfig`. Defaults, validation annotations and key names carry over unchanged; `application*.yaml` is unchanged. This follows the module sub-prefix rule already stated in the `RecoveryProperties` Javadoc ("no module reads another's") and avoids a cross-module configuration type. Class names are a plan detail. | [CODE]; Finding 019 plan input 9; ASM-04 |
| SPEC-RWB-TE-001-024 | **Coverage tests for relocated classes (finding 020).** Unit tests in the `test` task (JUnit 5, Mockito, Spring `ApplicationContextRunner` or MVC slice with `spring-boot-starter-webmvc-test` and `spring-security-test`, `temporal-testing`; no Docker, no database, no network) for each class below the gate, at its new home: `access.api.ApiError`, `ApiProblemException`; `access.internal.ApiExceptionHandler`, `ProblemFactory`, `SecurityConfig` and its properties record (401 problem without a token, CORS origins, roles-claim mapping; no call to an identity provider); `integration.flags` flag binding and `RecoveryFlags` bean; `integration.internal.PlatformInfoController` (mocked `JdbcTemplate`); `casewf.migration.RecoveryFlywayConfig` (configuration built without running `migrate`: schema placeholder, history table `flyway_schema_history_recovery`, clean disabled, location); `casewf.admin.TemporalAdminController` (each endpoint and the 503 MSG-P3-036 path); `casewf.workflow.internal.TemporalConfig`, `TemporalProperties`; `casewf.workflow.WorkflowIds`; `dochub.storage.BlobDocumentStore` and its configuration (mocked Blob clients: standard put, legal put, legal overwrite refused, get present and absent). Test data synthetic. Acceptance is SPEC-020 passing with no class excluded; existing tests stay as they are. | [TS] §3, §6; [BS] BS-7.2; [IEG]; finding 020 |
| SPEC-RWB-TE-001-025 | **Initial published lists equal what exists.** After SPEC-022 the published packages that hold types are exactly: `casewf.rules`, `casewf.timers`, `casewf.workflow` (D36 §3.3), `integration.flags.api` ([V7 E1-047] §12), `access.api`, `dochub.api`; every module's `api` exists with `package-info`. The map lists these (Field-level matrix), so SPEC-004 (d) passes on main classes. The public types in them are exactly: `casewf.rules` — `RuleEngine` (+ `RuleCompilationException`), `RuleInput`, `RuleOutcome`, `RuleResult`, `CompiledRulePackage`; `casewf.timers` — `TimerScheduler` (+ `TimerDue`); `casewf.workflow` — `WorkflowIds`; `integration.flags.api` — `RecoveryFlags`; `access.api` — `ApiError`, `ApiProblemException`; `dochub.api` — `DocumentStore` (+ its nested records and exception). No Temporal, Quartz or Drools implementation type is public in a published package (finding 030). `DroolsRuleEngine` and `DroolsProperties` stay package-private in `casewf.rules`, so they are not reachable from another package. The signature gap of `RuleEngine` and `TimerScheduler` against D36 §3.3 stays with RWB-E1-072 and RWB-E1-028 (DG-08). | Finding 019, 030; BR6; D36 §3.3 |
| SPEC-RWB-TE-001-026 | **`RecoveryBoundaryTest` on this repository.** Extend the existing class `th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryTest`: add the module-map rule, BND-1, BND-2, BND-4, BND-5 built from the real map; replace `blobClientOnlyInDocumentsModule` with BND-5 (SPEC-009); keep `noRecoveryClassNamesAPublicTable` unchanged (RWB-E1-069 owns it); keep `workflowImplementationsAreDeterministic` (BS-6.1) with its package retargeted from `recovery.workflow..` to `recovery.casewf.workflow..` (the workflow code's new home, [V7 E1-071] BR1). The `..` form includes `casewf.workflow.internal`, so `PlatformSmokeWorkflow.Impl` stays under the rule. The determinism rule is not a BND rule and RWB-E1-071 owns its final form (its WorkflowBoundaryTest). Its package string is a BS-6.1 rule input, not a module definition; BR6 covers module names, packages and published packages. | Finding 022, 024; [BS] BS-6.1; [V7 E1-071] BR1, §13 |

### Relocation table (SPEC-022)

All packages are under `th.co.scb.ace.demo.recovery`. "pp" = package-private. Visibility is unchanged except the two rows marked in bold (SPEC-022 (c)).

| Class today | New package | Module | Visibility | Source for the home |
|---|---|---|---|---|
| `rules.api.RuleEngine` (+ nested `RuleCompilationException`), `RuleInput`, `RuleOutcome`, `RuleResult`, `CompiledRulePackage` | `casewf.rules` (published) | P3 | public | D36 §3.3 (`RuleResult`, `RuleEvaluator`, `RuleCatalog` in `recovery.casewf.rules`); [V7 E1-072] §13 |
| `rules.internal.DroolsRuleEngine`, `DroolsProperties` | `casewf.rules` | P3 | pp | [V7 E1-072] §13: runtime, evaluator and catalog in `recovery.casewf.rules` |
| `platform.api.TimerScheduler` (+ nested `TimerDue`) | `casewf.timers` (published) | P3 | public | D36 §3.3; [V7 E1-028] §3, §12 |
| `platform.internal.QuartzTimerScheduler` (+ nested `TimerDueJob`) | `casewf.timers.internal` (not published) | P3 | pp (nested job public, as today; the package is not published, SPEC-022 (c)) | [V7 E1-028] §3, X10: the port and its Quartz job live under `recovery.casewf.timers`; finding 030 |
| `workflow.api.WorkflowIds` | `casewf.workflow` (published) | P3 | public | [V7 E1-071] §13, BR1; D36 §3.3 |
| `workflow.internal.PlatformSmokeWorkflow` (+ `Impl`, `Activities`, `SmokeResult`) | `casewf.workflow.internal` (not published) | P3 | public, as today | [V7 E1-071] §13 (worker and codec under `recovery/casewf/workflow`), BR1; D36 §3.3; finding 030 |
| `workflow.internal.PdpaPayloadCodec` | `casewf.workflow.internal` (not published) | P3 | **pp** (public today; class and constructor narrowed, SPEC-022 (c)) | As above; finding 030 |
| `workflow.internal.TemporalConfig` (+ nested `SmokeActivities`) | `casewf.workflow.internal` (not published) | P3 | pp | [V7 E1-071] §13 (worker) |
| `workflow.internal.TemporalProperties` | `casewf.workflow.internal` (not published) | P3 | **public** (pp today; read by `casewf.admin.TemporalAdminController`, SPEC-022 (c)) | [V7 E1-071] §13 |
| `workflow.internal.TemporalAdminController` | `casewf.admin` | P3 | pp | [V7 E1-071] §13 (endpoint in `recovery/casewf/admin`); [API] `x-module: P3` |
| `platform.internal.RecoveryFlywayConfig` | `casewf.migration` | P3 | pp | [V7 E1-044] §13; INC-001 spec ASM-E044-01 defers the home to this story |
| `platform.api.RecoveryFlags` | `integration.flags.api` (published) | P2 | public | [V7 E1-047] §12–§13 (flags in `recovery.integration.flags`, published `.api`); ASM-03 |
| `platform.internal.PlatformConfig` | `integration.flags` | P2 | pp | [V7 E1-047] §13; ASM-03 |
| `platform.internal.PlatformInfoController` | `integration.internal` | P2 | pp | ASM-02 (no source names a home; local operational endpoint, [README] item 6) |
| `platform.api.ApiError`, `ApiProblemException` | `access.api` | P4 | public | ASM-01 (gap DG-05) |
| `platform.internal.ApiExceptionHandler`, `ProblemFactory`, `SecurityConfig` | `access.internal` | P4 | pp | ASM-01 (gap DG-05) |
| `platform.internal.RecoveryProperties` | split (SPEC-023) | P2, P3, P4 | pp records | ASM-04 |
| `documents.api.DocumentStore` (+ nested records, exception) | `dochub.api` | P5 | public | [S] §13 (P5 `dochub`, published `api`) |
| `documents.internal.BlobDocumentStore` (+ nested configuration and `BlobProperties`) | `dochub.storage` | P5 | pp | [V7 TE-012] §13 (`recovery.dochub.storage`); `clientPackages` P5 `[storage]` |

**Why relocation rather than mapping the baseline modules (finding 019 option (b)).** Option (b) cannot satisfy the sources: D-RCV-36 §3.3 (highest precedence, [RB]) fixes the published packages `recovery.casewf.rules`, `recovery.casewf.timers` and `recovery.casewf.workflow`; [S] §13 and D-RCV-02 make the module name the package with codes P1..S9; `platform` holds P2, P3 and P4 code, so no one code fits it; `rules` and `workflow` would be two Modulith modules for one design module (P3), and L-RCV-14 rejects any module beyond the 19. Relocation renames only where a source requires it, keeps every behaviour, and lets the boundary test pass on the code (SPEC-025, T-TE001-05). It satisfies BND-1 and BND-2 (no collection or common dependency), BND-4 (no entity or repository), and BND-5 (`com.azure.storage` only in `dochub.storage`).

## Detailed design

### Components

| Component | Scope | Location | Responsibility |
|---|---|---|---|
| 19 module packages | main | `backend/src/main/java/th/co/scb/ace/demo/recovery/<name>/{,api/,internal/}package-info.java` | SPEC-001 |
| Relocated classes | main | Relocation table | SPEC-022, -023 |
| `recovery-modules.yaml` | test resource | `backend/src/test/resources/architecture/` | SPEC-002 |
| `ModuleMapLoader`, rule factory | test | a tooling package under `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/` (plan names it) | SPEC-003..-010 |
| `RecoveryBoundaryTest` | test | existing class, extended | SPEC-026 |
| Fixtures and fixture maps | test | fixture root outside `th.co.scb.ace.demo`; `…/architecture/fixtures/` | SPEC-011 |
| Coverage tests | test | test packages matching the new homes | SPEC-024 |
| Frontend fixture test | test | `frontend/src/modules/recovery/__tests__/` | SPEC-015 |
| Coverage tasks | build | `backend/build.gradle.kts` | SPEC-020 |

### Data and migration

No database object and no migration ([S] §11). `RecoveryFlywayConfig` moves package only; its bean, schema placeholder and history table are unchanged.

### Security and authority

No runtime authorization added or changed. `SecurityConfig` moves package with identical behaviour; its coverage tests assert the existing behaviour. Authority over the map: RW-TRIBE authors; code owners (RWB-TE-002, D-RCV-21) approve; the ACE team names common and collection packages (DL05).

### Observability, performance, feature flag

Output is the test report and ESLint output. No runtime metric, no flag; rollback is a revert merge request. The plan records the boundary test duration.

### No UI change

`DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-001-01 | AC1, BR1 | Unit (fixture) | `recovery.casewf.internal.SampleService` → `collection.internal.CollectorRepository` | BND-1 fails; text names BND-1, both classes |
| TC-TE-001-02 | AC2, BR2 | Unit (fixture) | `SampleService` → interface in `common.api` | Passes |
| TC-TE-001-03 | AC3, BR3 | Unit (fixture) | `recovery.integration.internal` class → `recovery.decision.internal.DecisionLogRepository`; then → `recovery.decision.writer.DecisionLogWriter` (published in fixture map and `@NamedInterface`) | `verify()` fails (Modulith text); then passes |
| TC-TE-001-04 | AC4, BR4 | Unit (fixture) | `recovery.integration.internal` class using `@Entity recovery.casewf.internal.RecoveryCaseEntity`; and an entity outside the recovery root | BND-4 fails on both |
| TC-TE-001-05 | AC5, BR5 | Unit (fixture) | `java.net.http.HttpClient` and a `com.azure.storage` type in `recovery.casewf.internal`; same in `recovery.integration.adapter` | Fails in `casewf`; passes in `integration.adapter` |
| TC-TE-001-06 | AC6 | Unit (frontend, Vitest) | `src/modules/recovery/caselist/<File>.tsx` importing `@/modules/collection/worklist/WorkList` and `../../collection/worklist/WorkList` | `no-restricted-imports` error for each |
| TC-TE-001-07 | AC7, BR6 | Unit (fixture) | Package `recovery.vendorx` absent from the fixture map | Fails: `… recovery.vendorx is not in the module map` |
| T-TE001-01 | SPEC-003 | Unit | Valid map; with `sourceViews`; missing file; invalid YAML; missing field; duplicate code; duplicate name; bad pattern; `internal` as published; unknown key | Valid and `sourceViews` pass; each error names file and field |
| T-TE001-02 | SPEC-004 | Unit (fixture) | Map module without package; type in root package; `@NamedInterface` package not in map; published package without `@NamedInterface`; classes only in a sub-package of an unmapped package; public type in a module base package; type-level `@NamedInterface`; a published package whose `@NamedInterface` leaves `propagate` at its default | Each fails with its text; a package-private type in a base package passes; a public type in an unlisted sub-package of a published package (for example `casewf.workflow.internal`) passes the map rule and is internal to its module |
| T-TE001-03 | SPEC-005, -006 | Unit (fixture) | Collection and common roots with no classes | Pass (`allowEmptyShould`) |
| T-TE001-04 | SPEC-010 | Unit (fixture) | Two violations of one rule | Both reported in one run in SPEC-010 text |
| T-TE001-05 | SPEC-001, -004, -009, -022, -025, -026 | Unit | Real main classes and real map | `RecoveryBoundaryTest` passes (all rules, including BND-5 with `BlobDocumentStore` in `dochub.storage`, determinism and BND-6 regex) |
| T-TE001-06 | SPEC-007, -018, -022 | Build | `./gradlew test`; a search of `backend/src` for string literals naming an old package (SPEC-022 (f)) | Whole suite green, including `ModulithTest` on the relocated modules and the moved unit tests (`DroolsRuleEngineTest` compiles its workbook with the renamed `Import` and `Variables` rows); the search finds nothing |
| T-TE001-07 | SPEC-014, -015 | Unit (frontend) | Rejected and allowed sets of SPEC-015 | Rejected each error; allowed none |
| T-TE001-08 | SPEC-013..-015, -020 | Build | `npm run check` | Green; frontend coverage at or above 80% on all four metrics, as printed |
| T-TE001-09 | SPEC-009 | Unit (fixture) | `casewf` class using `java.net.URLEncoder`, `java.net.SocketTimeoutException`, `java.net.URL`, a nested class of a listed class entry | First two pass; last two fail |
| T-TE001-10 | SPEC-020, -024 | Build | `./gradlew test recoveryCoverageVerification` | LINE, INSTRUCTION, BRANCH, METHOD each ≥ 80% over all recovery main classes plus tooling; report saved |
| T-TE001-11 | SPEC-018, -022 (h) | Build | `./gradlew recoveryIntegrationTest` (Docker) and `./gradlew e2eTest` on the local stack | Green; `/platform/info` and `/admin/temporal/health` answer as before |
| T-TE001-12 | SPEC-023, -024 | Unit | Bind each new properties record from the existing keys | Values equal those bound by `RecoveryProperties` today |
| T-TE001-13 | §13 step 7; SPEC-012 (b); Flow 6 | Build, negative control (run by the Builder; probe files never committed) | Three runs of `./scripts/dev.ps1 test` on the story branch. **Run 1:** an uncommitted main class `th.co.scb.ace.demo.recovery.casewf.internal.BoundaryProbe` that declares a field of type `java.net.http.HttpClient` (a field, because an unused import leaves no trace in bytecode). **Run 2:** the backend probe removed; an uncommitted `frontend/src/modules/recovery/caselist/BoundaryProbe.tsx` with `import "@/auth/auth";` (an existing module outside the D-RCV-39 allow-list, so `typecheck` passes and `lint` is the step that fails). **Run 3:** both probes removed. | Run 1: exit code non-zero; the Gradle log has `Rule BND-5 broken: …BoundaryProbe depends on java.net.http.HttpClient…`. Run 2: Gradle green; `npm run lint` reports `no-restricted-imports` for `BoundaryProbe.tsx`; exit code non-zero. Run 3: exit code 0. The Builder records the three exit codes and log lines as implementation evidence and shows that neither probe is committed. The orchestrator merges only after a run like Run 3 (SPEC-012 (b)). |
| T-TE001-14 | SPEC-022 (c), -025 | Unit | Real main classes: public types in each published package, and the Modulith named interfaces of `casewf` | The public types equal the SPEC-025 list; `ApplicationModules.of(AceRecoveryApplication.class)` reports for `casewf` the named interfaces `api`, `rules`, `timers`, `workflow`, and none of them contains a type from `casewf.workflow.internal` or `casewf.timers.internal` |

## Human verification items

These items cannot be tested in this repository. They are never reported as tested or passed.

| ID | Item | Why it is not tested here | Who verifies, and how | Status |
|---|---|---|---|---|
| HV-01 | The GitLab project that hosts the recovery module blocks a merge request whose pipeline fails (merge setting "Pipelines must succeed", or an equivalent required check), so a failing `backend-unit` or `frontend-check` job blocks the merge ([S] §13 step 7). | It is a setting of the hosting project, outside the repository. No GitLab MCP is connected (RUN-BRIEF rule 5): `N/A`. | The ACE platform or DevOps owner checks the setting on the first merge request that carries this story and records the result in the pull request (AGENTS.md §8). | OPEN (human) |

The local part of step 7 is tested: T-TE001-13 and SPEC-012 (b).

## Guardrails

- No business value in code; names, packages, client packages and libraries are in the map.
- No personal data in code, tests, fixtures or logs; class and package names and synthetic values only.
- Breaking fixtures stay in `src/test` (backend) or as string constants in the frontend test.
- No new endpoint, dependency, pipeline change or migration. No behaviour change in relocated code.

## Out of scope

SPEC-RWB-TE-001-016.

## Traceability

| Requirement ID | Requirement (short) | Source rule | SPEC | Tests |
|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | BR5, AC5 | SPEC-009, -010, -011, -022 | TC-TE-001-05; T-TE001-05, -09 |
| CTX-CONSTRAINT-002, CTX-DELIVERY-004 | Modular monolith; boundaries checked at build time | BR1–BR4, AC1–AC4, AC6 | SPEC-001, -004..-008, -010..-015, -022, -025, -026 | TC-TE-001-01..-04, -06; T-TE001-02..-08, -14 |
| [S] §13 step 7, "Done when" | A failing check blocks the merge | Flow 6 | SPEC-012 | T-TE001-13 (local); HV-01 (host, human) |
| BR-RWB-014 → FR-RWB-020 | No hard-coded values | BR6, AC7 | SPEC-002, -003, -004 | TC-TE-001-07; T-TE001-01 |
| [AUD] A-01, A-02 | Map the technical slices; module map and BND-1/2/4 | — | SPEC-002..-009, -022..-025 | T-TE001-05, -06 |
| [TS] §1, §6 | 80% coverage on recovery packages | — | SPEC-020, -024 | T-TE001-08, -10, -12 |
| D-RCV-52 | Access guard moved | X7, Flow 5 | SPEC-016 | — (RWB-E1-022) |

The traceability matrix groups TE-001 under BR-RWB-013 / FR-RWB-013 "for continuity" while the story's own source is REQ-DRI-006 ([S] §18); the rows to add are in `shared-updates.md` SU-01.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4; SPEC-008 | Does BND-4 forbid all non-own-module entities and repositories? | Later stories' data access | D-RCV-38 (recovery tech lead, 2026-11-09): option A, yes. | RESOLVED | SPEC-008 |
| CLAR-002 | Flow 4; AC6; SPEC-014 | Frontend allow-list for a repository without `src/modules/collection` | Which folders recovery may import | D-RCV-39: allow-list as in SPEC-014. | RESOLVED | SPEC-014 |
| CLAR-003 | §13 step 5; SPEC-015 | How the frontend fixture is proved | Test runner | D-RCV-40: Vitest + ESLint Node API. Vitest already present here; no new dependency. | RESOLVED | SPEC-015 |
| CLAR-004 | BR1; SPEC-005 | Collection root and published packages | BND-1 target | D-RCV-41: `th.co.scb.ace.demo.collection`, `[api]`. | RESOLVED | SPEC-002, -005 |
| CLAR-005 | BR3, AC3, §14 | BND-3 engine and text | Failure text | D-RCV-42: Modulith `verify()` only; its text accepted. | RESOLVED | SPEC-007 |
| CLAR-006 | BR5; SPEC-009 | Client library list | Map entries for later stories | D-RCV-41: 16 entries incl. Azure Storage and Kafka. | RESOLVED | SPEC-002, -009 |
| CLAR-007 | Flow 5, X7, TC-TE-001-08 | Access guard | Runtime code | D-RCV-52: moved to RWB-E1-022. | RESOLVED (moved out of scope) | SPEC-016 |
| CLAR-008 | Flow 2 | Map location | Packaging | D-RCV-37. | RESOLVED | SPEC-002 |
| CLAR-009 | Flow 6, §13 step 7 | Pipeline change | CI edits | D-RCV-05: none; CI already runs `test` and `npm run check`. | RESOLVED | SPEC-012 |
| CLAR-010 | §13 Package | Story placeholder paths | File paths | D-RCV-02, D-RCV-10. | RESOLVED | SPEC-001, -013 |
| CLAR-011 | BR1, BR2 | Empty collection/common packages | Rule on empty sets | D-RCV-19: `allowEmptyShould(true)`. | RESOLVED | SPEC-005, -006 |
| CLAR-012 | A-01; SPEC-022 | Homes of the baseline `platform`, `rules`, `workflow`, `documents` code | Package moves | Settled by precedence: D36 §3.3 and v7 stories (Relocation table). No question asked (L-RCV-03). | RESOLVED (precedence) | SPEC-022, -025 |
| CLAR-013 | DG-05; SPEC-022 | Module of error handling and `SecurityConfig` | Package of five classes | No source names it. Assumption ASM-01 (P4 `access`); open item for the recovery tech lead (`shared-updates.md` SU-02). | RESOLVED (assumption) | SPEC-022 |
| CLAR-014 | SPEC-022 | Home of `PlatformInfoController` | Package of one class | No source names it. Assumption ASM-02 (P2 `integration.internal`). | RESOLVED (assumption) | SPEC-022 |
| CLAR-015 | Finding 030; SPEC-001, -004 (d), -022 (c), -025 | How to keep Temporal and Quartz implementation types off the published surface | Package and visibility of four types; `@NamedInterface` form | Orchestrator triage (Claude Code, 2026-11-17T23:57, [BLOG]): make them non-public or move them out of the published packages, chosen by the BND rules. Settled by BND-3 (D-RCV-11), D36 §3.3 and [V7 E1-071] BR1: implementation moves to non-published sub-packages, published packages declare `propagate = false` (ASM-09), `PdpaPayloadCodec` becomes package-private. No question asked (L-RCV-03). | RESOLVED (precedence and triage) | SPEC-001, -004, -022, -025 |
| CLAR-016 | Finding 032; [S] §13 step 7; SPEC-012 | How "a failing fixture blocks a merge" is shown without a GitLab connection | Evidence for step 7 | Orchestrator triage ([BLOG]): locally, `./scripts/dev.ps1 test` exits non-zero on a violation and the orchestrator merges only on green (T-TE001-13); host-side blocking is HV-01 (human), never claimed as tested. | RESOLVED (local) / HV-01 OPEN (human) | SPEC-012 |

## Status reporting

```text
MCP_STATUS_SUMMARY: No Jira, Confluence, GitLab or Figma MCP connected (RUN-BRIEF rule 5); N/A. Repository-enabler story with no UI.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New build-time capability on the platform baseline: 19-module skeleton, relocation of the four baseline modules to their design homes, module map and map-driven boundary rules, AC6 fixture test, coverage lift. No screen, no API change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: build-time rules and package relocation without behaviour change]
REQUIREMENT_COVERAGE_SUMMARY: BR1-BR6 and AC1-AC7 mapped (AC3 and AC6 with accepted deviations D-RCV-42, D-RCV-39); X1-X6 mapped; X7/TC-TE-001-08 moved out of scope to RWB-E1-022 (D-RCV-52).
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] [COVERED_RULES: 13] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 2] [ASSUMPTIONS: 9] [HUMAN_VERIFICATION: 1]
```

`TOTAL_RULES: 13` counts BR1–BR6 and AC1–AC7. The same count is used in `compliance-validation.md`. `OPEN_ITEMS: 2` are the open-item rows requested in `shared-updates.md` SU-02 (DG-05) and SU-13 (HV-01); neither is a blocker. `HUMAN_VERIFICATION: 1` is HV-01 (host-side merge blocking). It does not block the spec, and it is never reported as tested.
