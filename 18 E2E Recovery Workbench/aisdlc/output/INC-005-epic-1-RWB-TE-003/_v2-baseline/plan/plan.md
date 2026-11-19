---
title: "Implementation Plan — RWB-TE-003 Types and contract tests from the API specification"
run_id: "INC-005-epic-1-RWB-TE-003"
story: "RWB-TE-003"
status: "SUCCESS"
---

# Implementation Plan — RWB-TE-003 Types and contract tests from the API specification

Design Source: NOT_REQUIRED (`UI In Scope: NO`, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`).

| Field | Value |
|---|---|
| Story | `RWB-TE-003` Types and contract tests from the API specification |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Input spec | `output/INC-005-epic-1-RWB-TE-003/specify/spec.md` (`SPEC-RWB-TE-003-001..013`, 8 ACs, 8 exception paths) |
| Governing decisions | D-RCV-05, D-RCV-06, D-RCV-11, D-RCV-37, D-RCV-39, D-RCV-40, D-RCV-43; L-RCV-11, L-RCV-14 |
| Baseline | Document set v14, 16 November 2026; API Specification v4; TE-001 module map |
| Prepared | 2026-11-17, Implementation Planner (agent run) |
| Approval | Plan gate pending human; no question asked |

## Plan approval preconditions

| ID | Precondition | Owner | State | Evidence when met |
|---|---|---|---|---|
| PRE-1 | Specification approval (specification gate) | Product Owner | APPROVED for the v2 baseline 2026-11-17 | `specify/compliance-validation.md` `PASS` |
| PRE-2 | `api/recovery-api.yaml` is the canonical repository copy of API Specification v4 and matches the document-set file | Recovery tech lead / API owner | **PENDING** — `OPEN-039` | Byte-equality check output |
| PRE-3 | Generator and validator versions are approved and pinned: OpenAPI Generator, swagger-request-validator, openapi-typescript, openapi-fetch | Forward Deployed Architect | **PENDING** — `OPEN-039` | Version list in the plan approval |
| PRE-4 | `L-RCV-11` enforcement baseline accepted: E1 operations are pending with a named story until enforced | Recovery tech lead | **PENDING** — `OPEN-039` | Plan approval comment |
| PRE-5 | P2 `integration` published packages `generated.web`/`generated.model` accepted in the TE-001 module map | Recovery tech lead | **PENDING** — `OPEN-039` | Module-map review |
| PRE-6 | Live access case `TC-TE-003-09` accepted as blocked until E1-022/E1-037 | QA lead / recovery tech lead | **PENDING** — `OPEN-040` | Plan approval comment |
| PRE-7 | Plan approval | Forward Deployed Architect | **PENDING HUMAN** | Approval comment in the increment card |
| PRE-8 | Task approval | Forward Deployed Engineer | **PENDING HUMAN** | Approval comment in the increment card |
| PRE-9 | API file code-owner approval (TE-002) | Recovery tech lead | **PENDING** — TE-002 plan | TE-002 branch rule/code-owner review |

`TASK-RWB-TE-003-00` checks PRE-1..PRE-9. If PRE-2..PRE-6 are not approved, the plan is complete but
the build does not start. This is a gate, not a question to the user.

## Change scope

| Field | Value |
|---|---|
| Change type | `NEW_STORY` |
| UI in scope | NO |
| Logic in scope | YES — lint, generation, catalog, baseline, contract/access tests, report |
| API in scope | YES — the API specification is the generated contract source; no endpoint change |
| API impact | `NO_API_CHANGE` |
| Frontend changes | YES — generator wrapper, generated types/client (gitignored), build wiring; no screen |
| Backend changes | YES — build/test tooling, generated interfaces/models, contract/access suites; no production endpoint |
| Migration / database | None |
| New dependencies | Pinned at PRE-3; no new runtime service |

## Scope

### In scope

1. `api/recovery-api.yaml` copied from API Specification v4 and kept byte-equal to the document set.
2. `api/recovery-api-implementation.yaml`: 73 E1 operations, owning story, `enforce` flag.
3. `RecoveryApiLint` for BR2, run before generation.
4. Server generation: Spring interfaces/models, interface-only, one interface per tag, P2 `integration.generated.web`/`.model`.
5. Front-end generation: TypeScript types and typed client in `frontend/src/modules/recovery/api/generated`.
6. `OperationCatalog`, `ContractBaseline`, `ImplementedOperationResolver`.
7. `RecoveryContractTest` and fixtures for AC2/AC4/AC5.
8. `RecoveryAccessContractTest` and the fixture security check for AC8.
9. Contract report: passed, failed, pending, story.
10. Module map update: P2 `published` gains `generated.web`/`generated.model`; generated `package-info.java` files.
11. Build wiring into `check`; no pipeline change (D-RCV-05).
12. Backend/frontend unit tests and 80% coverage.
13. Determinism re-run and evidence pack.
14. Live access case `TC-TE-003-09` recorded blocked until E1-022/E1-037.

### Out of scope

- Any endpoint, controller, entity, migration or screen.
- File-interface contract tests (RWB-E1-007).
- Browser tests (RWB-TE-010).
- Permission matrix content (RWB-E1-037).
- A new API version or a contract change.
- A new workflow, rules engine or runtime service.

## Backend plan

### B-1 API file and baseline

| Item | Value |
|---|---|
| API file | `api/recovery-api.yaml`; source `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Equality check | `cmp`/hash against the document-set copy; a drift fails the lint |
| Baseline | `api/recovery-api-implementation.yaml`; 73 E1 rows; `story` and `enforce: false` initially |
| Source of story | Build Sequence v6 and the story set; no inferred story names |
| Validation | Every E1 operation has exactly one row; no duplicate; no non-E1 row in the E1 baseline |

### B-2 Lint

| Rule | Failure |
|---|---|
| Missing/duplicate `operationId` | `lint rule broken: {operation} operationId` |
| Missing `x-module` (P1–P10 or S1–S9) | `lint rule broken: {operation} x-module` |
| Missing `x-capability.area`/`right`; `None` only with `R` | `lint rule broken: {operation} x-capability` |
| Missing/invalid `x-first-release` | `lint rule broken: {operation} x-first-release` |
| Unresolved `$ref` | `lint rule broken: {operation} $ref` |
| No 4xx/5xx response | `lint rule broken: {operation} error response` |
| Error response not `application/problem+json` + `Problem` | `lint rule broken: {operation} problem schema` |

### B-3 Generation and module map

| Item | Value |
|---|---|
| Gradle plugin | `org.openapi.generator`, pinned at PRE-3 |
| Generator | `spring`, `interfaceOnly=true`, `useSpringBoot3=true`, `useTags=true`, `generateApiTests=false`, `generateModelTests=false` |
| Packages | `th.co.scb.ace.demo.recovery.integration.generated.web`, `.generated.model` |
| Package info | Generator wrapper writes `@NamedInterface("generated.web")` and `@NamedInterface("generated.model")` |
| Module map | Add `generated.web` and `generated.model` to P2 `integration` `published`; no new module |
| Boundary test | TE-001 map rule accepts the two published packages; no dependency on `internal` |

### B-4 Catalog, baseline and resolver

| Class | Package | Responsibility |
|---|---|---|
| `OperationCatalog` | `recovery.contract` (test) | Read the OpenAPI file; group by release; expose operationId, capability, story and responses. |
| `ContractBaseline` | `recovery.contract` (test) | Read `api/recovery-api-implementation.yaml`; answer enforced/pending/story; fail on a missing E1 row. |
| `ImplementedOperationResolver` | `recovery.contract` (test) | Find controller beans implementing generated interfaces; map method name to operationId. |
| `ContractFixtures` | `recovery.contract` (test) | Synthetic request/response per operation; resettable; no production data. |
| `RecoveryContractTest` | `recovery.contract` (test) | Parameterised per enforced implemented operation; validate request/response/status/content type/schema. |
| `RecoveryAccessContractTest` | `recovery.contract` (test) | Parameterised per enforced implemented operation; 403 + Problem + MSG-P4-002. |
| `RecoveryApiReport` | `recovery.contract` (test/build) | Write `build/reports/recovery-contract/contract-report.json`/`.md`. |

### B-5 Contract and access suites

- `RecoveryContractTest` uses `MockMvc` and the generated interface. A fixture controller can return raw
  JSON for AC2/AC4 negatives; the live path uses the generated model.
- The failure text is exact: `contract broken: {operationId} at {path}: {reason}` and
  `undocumented status {status} for {operationId}`.
- `RecoveryAccessContractTest` reads `x-capability`; selects a role from the permission matrix seed or a
  synthetic fixture that lacks the right; expects 403, `application/problem+json`,
  `messageCode = MSG-P4-002`; a 200 fails `access not enforced for {operationId}`.
- An operation with `x-capability.area: None` is authentication-only: the suite records
  `NOT_APPLICABLE_AUTHENTICATED` and tests 401 without a session; it does not record a 403 pass. The v4
  operations are `getFeatureFlags` and `getMeSession` (`ASM-TE003-09`, `OPEN-042`).
- The fixture security configuration is test-scope only; the live guard is RWB-E1-022's.
- `TC-TE-003-09` is recorded blocked until E1-022/E1-037; no mocked role is recorded as passing.

### B-6 Report and build wiring

| Task | When | Failure |
|---|---|---|
| `recoveryApiLint` | Before `openApiGenerate` | BR2 rule |
| `openApiGenerate` | After lint | Generator |
| `recoveryContractTest` | `test`/`check` | Enforced missing or contract mismatch |
| `recoveryAccessContractTest` | `test`/`check` | Access not enforced |
| `recoveryApiReport` | After both suites | Writes pass/fail/pending; failed suite fails build |

No pipeline file change (D-RCV-05). `rwb.release` defaults to `E1`; overridable by Gradle property or
environment, never a business literal in code.

## Frontend plan

Frontend component inventory: `NOT_APPLICABLE` (`UI In Scope: NO`, 0 screens); no
`frontend/components.md`. The front-end work is a build generator and typecheck fixture, not a screen.

### F-1 Generator wrapper

| Item | Value |
|---|---|
| Location | `frontend/scripts/recovery-api/` (hand-written wrapper and test) |
| Output | `frontend/src/modules/recovery/api/generated/schema.d.ts`, `client.ts` (gitignored) |
| Tool | `openapi-typescript` + `openapi-fetch`, pinned at PRE-3 |
| Behaviour | Read `api/recovery-api.yaml`; write deterministic files; no network; fail on an unresolved `$ref` |
| Build | Run before `typecheck`; generated folder is not committed by default |

### F-2 Removed-field typecheck fixture

- A fixture screen under `frontend/scripts/recovery-api/__fixtures__/` imports the generated `Case` type
  and reads `legalHold`.
- A fixture spec removes `legalHold` from `Case`.
- `tsc --noEmit -p <fixture tsconfig>` must fail with the file and line; the live spec keeps `legalHold`
  in the generated type.
- This proves AC7 without a screen in the delivery.

### F-3 Frontend unit tests

- Vitest on `frontend/scripts/recovery-api/**`: generated `warnAt` appears; output is byte-identical on a
  second run; removed-field fixture fails; no network.
- 80% lines, statements, branches and functions on the wrapper.
- The generated output itself is not hand-written and is not unit-tested.

## Integration and cross-layer

| Item | Plan |
|---|---|
| TE-002 code owners | The API file and generated tooling are owned by the recovery team; a change to `api/recovery-api.yaml` needs code-owner review. |
| TE-001 module map | P2 `published` gains the two generated packages; map tests stay green. |
| E1 endpoint stories | Each story sets its operation rows to `enforce: true` and adds the controller; the contract/access suites then gate it. |
| E1-022/E1-037 | The live access case activates after the guard and matrix exist; `TC-TE-003-09` stays blocked until then. |
| Build | The tasks join `check`; no pipeline change. |
| Rollback | Revert the build wiring/baseline; generated code is not deployed until an endpoint story uses it. |

## Unit test applicability

| Surface | Changes required | Unit tests | Coverage gate | References | Evidence |
|---|---|---|---|---|---|
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on `recovery.contract` and lint task classes | SPEC-001..012; AC1–AC8 | JaCoCo `recoveryContractCoverageReport` |
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on `frontend/scripts/recovery-api/**` | SPEC-004, -013; AC1, AC7 | Vitest `coverage/recovery-api` |

Contract/access suites are integration/system tests and do not replace the unit gates.

## Requirement Logic To Task Coverage

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| BR1 | SPEC-001 | 01, 02, 03, 04 | DIRECT_IMPLEMENTATION | One API file; no duplicate DTOs; equality check | COVERED |
| BR2 | SPEC-002 | 03, 15 | DIRECT_IMPLEMENTATION | Lint fixtures for each rule | COVERED |
| BR3 | SPEC-005, -006, -007 | 02, 06, 08, 15 | DIRECT_IMPLEMENTATION | Baseline; contract suite; AC5/AC6 | COVERED |
| BR4 | SPEC-008 | 09, 15, 21 | DIRECT_IMPLEMENTATION | Access suite; 403 + MSG-P4-002 | COVERED |
| BR5 | SPEC-003, -004, -010 | 04, 11, 12, 20 | DIRECT_IMPLEMENTATION | Generated output; no hand edits; determinism | COVERED |
| AC1 | SPEC-003, -004, -013 | 04, 05, 11, 12, 13, 14 | DIRECT_IMPLEMENTATION | `warnAt` in both outputs | COVERED |
| AC2 | SPEC-007, -012 | 08, 10 | DIRECT_IMPLEMENTATION | Contract failure names path | COVERED |
| AC3 | SPEC-002 | 03, 15 | DIRECT_IMPLEMENTATION | Lint fails naming operation | COVERED |
| AC4 | SPEC-007, -012 | 08, 10 | DIRECT_IMPLEMENTATION | `undocumented status 400` | COVERED |
| AC5 | SPEC-005, -006, -007 | 02, 06, 08, 15 | DIRECT_IMPLEMENTATION | `getAdminJobs` baseline, no controller | COVERED |
| AC6 | SPEC-005, -006, -009 | 02, 06, 08, 10 | DIRECT_IMPLEMENTATION | E2 op pending; E1 build passes | COVERED |
| AC7 | SPEC-004, -013 | 12, 14, 19 | DIRECT_IMPLEMENTATION | Typecheck fixture fails | COVERED |
| AC8 | SPEC-008 | 09, 15, 21 | DIRECT_IMPLEMENTATION | Fixture 200 fails; live blocked | COVERED |
| Flow 1–8 | SPEC-001..-012 | 01–17 | DIRECT_IMPLEMENTATION | Lint, generate, compile, catalog, contract, access, report | COVERED |
| X1–X8 | SPEC-002, -006, -007, -008, -012, -013 | 03, 08, 09, 10, 14, 15 | DIRECT_IMPLEMENTATION | Fixture/report per exception | COVERED |
| §12 Contract | SPEC-001..-010 | 01–17 | DIRECT_IMPLEMENTATION | Contract fields implemented | COVERED |
| §17 Guardrails | SPEC-002, -010, -011 | 03, 05, 16, 20 | DIRECT_IMPLEMENTATION | No literal business value; synthetic fixtures; no hand edit | COVERED |
| §19 Out of scope | SPEC-012 | 22 | DIRECT_IMPLEMENTATION | Scope note in evidence | COVERED |

Every row is `COVERED`; no `BLOCKED` row. Every task maps to at least one SPEC.

## Functional Test Scenarios

| ID | Scenario | AC | Owner |
|---|---|---|---|
| T-TE003-01 | Add `warnAt`; both generated outputs hold it | AC1 | Backend/frontend build |
| T-TE003-02 | Wrong type `escalationLevel`; contract fails with path | AC2 | Contract suite |
| T-TE003-03 | Missing x-capability; lint fails | AC3 | Lint suite |
| T-TE003-04 | Undocumented 400; contract fails | AC4 | Contract suite |
| T-TE003-05 | Enforced `getAdminJobs`; no controller; fails | AC5 | Contract suite |
| T-TE003-06 | E2 operation pending; E1 passes | AC6 | Report |
| T-TE003-07 | Removed `legalHold`; typecheck fails | AC7 | Frontend typecheck fixture |
| T-TE003-08 | No access check; 200; `access not enforced` | AC8 | Access suite |
| T-TE003-09 | `RW-REFADM` calls `getCasesCaseidTimers` | Access | **BLOCKED** until E1-022/E1-037 |

## Security, privacy and compliance

- The access suite uses synthetic roles and the permission matrix seed/fixture; no production user.
- Fixtures are synthetic; no personal data, account number, secret or production data.
- The API file and generated code contain schema names and operationIds, not personal data.
- The report holds operationIds and paths only.
- No token or credential in the repository; generators use the build's normal dependency access.
- No new runtime service; generated code is behind the existing ACE API client boundary.

## Risks

| ID | Risk | Mitigation |
|---|---|---|
| R-01 | `L-RCV-11` baseline is not accepted | PRE-4 blocks; the alternative is to defer the story until endpoints exist. |
| R-02 | API file drifts from the document set | PRE-2 byte-equality check in the lint. |
| R-03 | Generator/validator versions change | Pinned at PRE-3; `git diff` on lockfiles only. |
| R-04 | Generated package breaks the TE-001 boundary | P2 published `generated.web`/`.model`; map tests. |
| R-05 | Live access test is mistaken for passing | `TC-TE-003-09` `BLOCKED`; no mocked pass. |
| R-06 | Contract suite is too slow as endpoints grow | One success call per enforced operation; synthetic fixtures; measure at each story. |
| R-07 | A controller method is not found (name mismatch) | Resolver test; `operation not in baseline` / `has no implementation`. |

## Out of scope

- Endpoints, controllers, entities, migrations, screens; file-interface contract tests; browser tests;
  permission matrix content; a new API version; a new runtime service.

## Assumptions

| ID | Assumption | Basis |
|---|---|---|
| `ASM-TE003-01` | Canonical `api/recovery-api.yaml` equals the document-set v4 file | Story §3; API v4 |
| `ASM-TE003-02` | Generators run in the existing build | TE-001; story §3 |
| `ASM-TE003-03` | Every E1 operation has a story in the baseline | Build Sequence v6 |
| `ASM-TE003-04` | Permission matrix seed; synthetic fixture until E1-037 | Story §3; E1-037 |
| `ASM-TE003-05` | operationId = Java method name; one interface per tag | Generator `spring` |
| `ASM-TE003-06` | P2 published generated packages | TE-001 map; `L-RCV-14` |
| `ASM-TE003-07` | `warnAt` already in v4 Timer | API v4 line 6602 |
| `ASM-TE003-08` | Dependencies pinned at PRE-3 | `AGENTS.md` §4.4 |
| `ASM-TE003-09` | `x-capability.area: None` is authentication-only; `getFeatureFlags` and `getMeSession` use it | API v4; BR4; `OPEN-042` |
| `L-RCV-03` | No question asked | No-question rule |

## Status reporting

```text
PLAN_STATUS: SUCCESS
TASKS: 23
SCOPE: one module (recovery.integration.generated + recovery.contract test scope) + named shared build files; no other ACE module
BLOCKED_TASKS: 0 (PRE-2..PRE-6 are human gates, not blockers to plan completion)
ASSUMPTIONS: 10
NEXT_STEP: Human plan approval, then start the Implementation Builder on TASK-00..22.
```

```text
PLANNER_STATUS_SUMMARY: Plan and tasks are complete for RWB-TE-003; build is gated on the API file, pinned dependencies, the L-RCV-11 baseline and the live access dependency.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: one build-tooling increment, no endpoint] [UNBLOCK_ACTION: approve plan and close OPEN-039]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI NO]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: All 18 spec coverage rows (32 statements) are mapped to tasks.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 18] [TASK_COVERED_RULES: 18] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
```
