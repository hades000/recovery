---
title: "Tasks — RWB-TE-003 Types and contract tests from the API specification"
run_id: "INC-005-epic-1-RWB-TE-003"
story: "RWB-TE-003"
---

# Tasks — RWB-TE-003

Design Source: NOT_REQUIRED (`UI In Scope: NO`).

Plan: `plan.md`. All paths are in the ACE repository unless they start with `output/` or `docs/`.
Task IDs are `TASK-RWB-TE-003-NN`; the short form `TASK-NN` in `plan.md` means the same task.

**Every build task is blocked by TASK-00 (plan-approval preconditions).** No business endpoint is
built. The story builds the API generation and contract/access tooling that later endpoint stories use.

## Task table

| TASK ID | Description | Trace (SPEC/FR/NFR) | BLOCKED_BY | Verification |
|---|---|---|---|---|
| `TASK-RWB-TE-003-00` | **Plan precondition check.** Confirm PRE-1 spec approval; PRE-2 API file canonical and byte-equal; PRE-3 pinned dependencies (OpenAPI Generator, swagger-request-validator, openapi-typescript, openapi-fetch); PRE-4 `L-RCV-11` baseline acceptance; PRE-5 P2 generated packages; PRE-6 live access block; PRE-7/PRE-8 plan/task approvals; PRE-9 TE-002 code-owner review. Confirm `OPEN-042` (authentication-only `area: None`) or record it as a lint finding. Record dates and the API file hash. Stop with `BLOCKED` if PRE-2..PRE-6 are unapproved. | SPEC-001, -005, -008, -011; D-RCV-05, -11, -37; `OPEN-039`, `OPEN-040`, `OPEN-042` | NONE | Decisions and hash in `output/INC-005-epic-1-RWB-TE-003/implement/report.md` |
| `TASK-RWB-TE-003-01` | **Place the canonical API file.** Copy `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` to `api/recovery-api.yaml`; do not edit it. Confirm byte equality and that the file is covered by TE-002 code owners. | SPEC-001; BR1; `ASM-TE003-01` | 00 | `sha256sum` equal; `git diff --exit-code` on the file; code-owner entry present |
| `TASK-RWB-TE-003-02` | **Create the E1 baseline.** Add `api/recovery-api-implementation.yaml` with `release: E1` and 73 rows (`operationId`, `story`, `enforce: false`) built from the Build Sequence and the story set. No duplicate, missing or non-E1 operation; every story key exists in the manifest. | SPEC-005, -006; BR3; AC5, AC6; `ASM-TE003-03` | 00, 01 | Script compares the 73 operationIds with the spec's E1 set: 73/73; duplicate check; story-key check |
| `TASK-RWB-TE-003-03` | **`RecoveryApiLint`.** Implement the seven BR2 checks (operationId, x-module, x-capability, x-first-release, `$ref`, error response, Problem) as a Gradle task that runs before `openApiGenerate`. Add fixture specs for each failure. | SPEC-002; BR2; AC3, X2 | 00, 01 | Fixture tests fail with the exact rule text; clean spec passes; task order `lint → generate` |
| `TASK-RWB-TE-003-04` | **Server generation.** Add the pinned OpenAPI Generator plugin/config: Spring interfaces, interface-only, Spring Boot 3, one interface per tag, generated packages `...integration.generated.web`/`.model`, no API/model tests. Make the service compile against the generated interfaces. | SPEC-003; BR5; AC1; `ASM-TE003-05` | 00, 01, 03 | `./gradlew openApiGenerate compileJava`; one interface per tag; model has `warnAt` |
| `TASK-RWB-TE-003-05` | **Generated packages and module map.** Add `generated.web` and `generated.model` to the P2 `integration` `published` list in `backend/src/test/resources/architecture/recovery-modules.yaml`; write `package-info.java` with `@NamedInterface("generated.web")`/`("generated.model")`; no new module. | SPEC-003, -011; BR5; `ASM-TE003-06`; L-RCV-14 | 04 | Map loads; published list has both; `RecoveryModuleMapTest`/`RecoveryBoundaryTest` green; `ModulithTest` green |
| `TASK-RWB-TE-003-06` | **Catalog, baseline and resolver.** Add `OperationCatalog`, `ContractBaseline`, `ImplementedOperationResolver` and `ContractFixtures` in `recovery.contract` (test scope). The catalog reads the 141 operations and selects by `rwb.release`; the baseline answers enforced/pending/story; the resolver maps generated interface methods to operationIds. | SPEC-005, -006; BR3; AC5, AC6 | 02, 04, 05 | `./gradlew compileTestJava`; unit tests in TASK-07 |
| `TASK-RWB-TE-003-07` | **Support unit tests.** `OperationCatalogTest` (141 operations, 73 E1, capability, story), `ContractBaselineTest` (73 rows, enforce flag, missing-row failure, non-E1 row failure), `ImplementedOperationResolverTest` (method-name match, no-match). Synthetic fixtures only. | SPEC-005, -006; BR3; AC5, AC6 | 06 | `./gradlew test --tests "th.co.scb.ace.demo.recovery.contract.*Test"` green |
| `TASK-RWB-TE-003-08` | **Contract suite.** `RecoveryContractTest` with `MockMvc`, generated interfaces and fixtures; validate request, response, status, content type and schema. Add fixture controllers for AC1/AC2/AC4/AC5, including a raw-JSON controller for the wrong type and the undocumented 400. Add `ContractFixtures` data. | SPEC-007, -012; BR3; AC2, AC4, AC5, X1, X3, X4 | 06 | Fixture tests fail with the exact text; clean fixture passes; report rows |
| `TASK-RWB-TE-003-09` | **Access suite.** `RecoveryAccessContractTest` with test-scope security; select a role lacking the declared right from the permission-matrix seed/fixture; expect 403, `application/problem+json`, `messageCode = MSG-P4-002`; a 200 fails `access not enforced`. An operation with `x-capability.area: None` (v4: `getFeatureFlags`, `getMeSession`) is authentication-only: record `NOT_APPLICABLE_AUTHENTICATED` and test 401 without a session; no 403 pass. Add a fixture controller with the check and one without. | SPEC-008; BR4; AC8, X7, X8; `ASM-TE003-04`, `ASM-TE003-09` | 06 | Fixture-without-check fails with `access not enforced`; fixture-with-check returns 403 + Problem; `area: None` rows show `NOT_APPLICABLE_AUTHENTICATED`; `TC-TE-003-09` recorded blocked |
| `TASK-RWB-TE-003-10` | **Report.** Add `RecoveryApiReport`: `build/reports/recovery-contract/contract-report.json` and `.md`; every E1 operation with `operationId`, release, story, `PASSED`/`FAILED`/`PENDING`, contract/access result and reason. AC6 pending row must appear. | SPEC-009; AC6; X5 | 08, 09 | Report schema check; pending row for `postQueuesQueueidPlacements`; failed suite fails build |
| `TASK-RWB-TE-003-11` | **Front-end generator wrapper.** Add `frontend/scripts/recovery-api/generate.mjs` (pinned `openapi-typescript`/`openapi-fetch`); read `api/recovery-api.yaml`; write `schema.d.ts`, `client.ts` and the package-info files; no network; deterministic. | SPEC-004; BR5; AC1, AC7 | 00, 01 | Run twice; `git diff --exit-code` on output; wrapper exits 0 on the clean spec |
| `TASK-RWB-TE-003-12` | **Front-end build wiring.** Add the pinned dev/runtime dependencies; gitignore `frontend/src/modules/recovery/api/generated`; run the wrapper before `typecheck`; add the generator/typecheck scripts to the frontend `check` target. Do not add a screen. | SPEC-004, -010; BR5; AC1, AC7 | 11 | `npm ci`; `nx run frontend:typecheck` green after generation; generated folder ignored; no screen file |
| `TASK-RWB-TE-003-13` | **Front-end wrapper unit tests.** Vitest on `frontend/scripts/recovery-api/**`: `warnAt` appears in `schema.d.ts`; second run byte-identical; no network; fixture spec failure. 80% lines/statements/branches/functions. | SPEC-004, -013; AC1; AC7 | 12 | `npx vitest run --coverage` green; coverage ≥ 80% on the wrapper |
| `TASK-RWB-TE-003-14` | **Removed-field typecheck fixture.** Add a fixture screen importing the generated `Case` type and reading `legalHold`; add a fixture spec without `legalHold`; run `tsc --noEmit -p <fixture tsconfig>` and confirm the failure names the file and line. The live spec keeps `legalHold`. | SPEC-013; AC7; X6 | 12 | Fixture command exits non-zero with the file/line; live typecheck passes |
| `TASK-RWB-TE-003-15` | **Negative fixtures for AC3/AC5/AC6.** Add a missing-`x-capability` operation; an enforced `getAdminJobs` row with no controller; an E2 `postQueuesQueueidPlacements` row outside the E1 baseline. Confirm lint fails, contract fails, and the E1 build passes with a pending row. | SPEC-002, -006, -007; AC3, AC5, AC6; X2, X4, X5 | 03, 08 | Fixture tests show each outcome; no change to the live spec |
| `TASK-RWB-TE-003-16` | **Boundary tests for generated packages.** Extend the TE-001 map/rule tests to accept the two P2 published packages and reject a dependency on `generated` from a non-published path or on `integration.internal`. No new module. | SPEC-011; BR5; D-RCV-11, -37 | 05 | `./gradlew test --tests "*.recovery.architecture.*"` green; negative fixture fails |
| `TASK-RWB-TE-003-17` | **Build integration.** Add `recoveryApiCheck` or join the tasks to `check` in the order lint → generate → contract → access → report. No pipeline file change. Add `rwb.release` with default `E1`; no business literal in code. | SPEC-010; D-RCV-05; BR5 | 10, 16 | `./gradlew check` runs the tasks in order; `git diff .gitlab-ci.yml .github/workflows` empty |
| `TASK-RWB-TE-003-18` | **Backend coverage gate.** JaCoCo on `recovery.contract` and the lint task classes; 80% lines/statements/branches/functions; save the XML/HTML and results table. | SPEC-001..-012; D-RCV-06/40 | 07, 08, 09, 15 | `recoveryContractCoverageVerification` green; XML ≥ 80%; evidence saved |
| `TASK-RWB-TE-003-19` | **Frontend coverage gate.** Vitest coverage on the wrapper; 80% lines/statements/branches/functions; save `coverage-summary.json` and the console log. | SPEC-004, -013; D-RCV-06/40 | 13, 14 | Coverage ≥ 80%; evidence saved; no generated file linted |
| `TASK-RWB-TE-003-20` | **Determinism and re-run.** Generate twice and compare hashes; run the contract/access/report twice; same result and same report content. Record durations. | SPEC-010; §12 Idempotency; BR5 | 17, 18, 19 | Hash equality; diff empty; second run green |
| `TASK-RWB-TE-003-21` | **Live access case record.** Record `TC-TE-003-09` as `BLOCKED` with the E1-022/E1-037 dependency; do not record a mocked role as a pass. Add the unblock action and owner. | SPEC-008; BR4; `OPEN-040` | 09 | Test matrix row `BLOCKED`; evidence note; no PASS claim |
| `TASK-RWB-TE-003-22` | **Evidence, trace and MR record.** Save the API hash, pinned versions, lint/generator/test/coverage logs, report artifacts and the blocked access note under `output/INC-005-epic-1-RWB-TE-003/implement/`. Update `requirement/Traceability_Matrix.md` row 005 and the increment card. Record the ACE branch/commit/MR when created. Do not commit, push or open an MR unless the user asks. | SPEC-001..-013; §17/§19; `CLAUDE.md` two-repository rule | 20, 21 | Evidence files present; matrix row updated; branch placeholder recorded |

## Dependency graph

```text
00 ─► 01 ─┬─► 03 ─► 04 ─┬─► 05 ─► 16 ─┐
          │             │             │
          ├─► 02 ───────┴─► 06 ─┬─► 07 ┤
          │                    ├─► 08 ─┼─► 10 ─► 17 ─┐
          │                    └─► 09 ─┘             │
          ├─► 11 ─► 12 ─┬─► 13 ──────────────────────┤
          │             └─► 14 ──────────────────────┤
          │                                         ├─► 20 ─► 22
          ├─► 15 ──────────────────────────────────┤
          └─────────────────────────────────────────┘
07,08,09,15 ─► 18 ─┐
13,14 ─► 19 ───────┴─► 20 ─► 22
09 ─► 21 ─────────────────────► 22
```

No cycle. Backend (03–10, 15–18) and frontend (11–14, 19) run in parallel after 01–02; 20 and 22 close.

## Coverage

| SPEC | Tasks |
|---|---|
| 001 | 00, 01, 18 |
| 002 | 03, 15, 18 |
| 003 | 04, 05, 17 |
| 004 | 11, 12, 13, 19 |
| 005 | 00, 02, 06, 07 |
| 006 | 02, 06, 07, 08, 15 |
| 007 | 08, 15, 18 |
| 008 | 09, 15, 18, 21 |
| 009 | 10, 17 |
| 010 | 12, 17, 20 |
| 011 | 00, 05, 16 |
| 012 | 08, 09, 10 |
| 013 | 13, 14, 19 |

Every SPEC has at least one task; no orphan task.

## Pre-submit checks

| Check | Result |
|---|---|
| Every SPEC-001..013 maps to a task | YES (13/13) |
| Every spec coverage row (18) maps to a task | YES (18/18) |
| Every task has `BLOCKED_BY` (`NONE` only for TASK-00) | YES |
| Every task has a verification method and trace links | YES |
| Every unit-test task is blocked by its implementation task | YES (07←06, 13←12) |
| Backend unit/coverage task present | YES (07, 18) |
| Frontend unit/coverage task present | YES (13, 19) |
| No endpoint/controller/screen/migration task | YES |
| API impact tasks | NONE — `NO_API_CHANGE` |
| Module map / generated-package task present | YES (05, 16) |
| `L-RCV-11` baseline task present | YES (02, 06) |
| Determinism task present | YES (20) |
| Live access case recorded blocked | YES (21) |
| Authentication-only `area: None` handled | YES (TASK-09; `OPEN-042`) |
| Design evidence | `NOT_APPLICABLE` — UI NO, 0 screens, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` |
| No question asked | YES |
| No real PII, secret or production data | YES |
