# API Test Report — RWB-TE-001

| Field | Value |
|---|---|
| RUN_ID | `INC-002-epic-1-RWB-TE-001` |
| Story / Epic | RWB-TE-001 / EPIC-001 |
| Stage | API Tester |
| Date | 2026-11-18 |
| Status | **NOT_APPLICABLE (N/A)** |
| API In Scope (spec) | `NO` |
| API Impact Type (spec) | `NO_API_CHANGE` |
| APIs / controllers / cases | 0 / 0 / 0 |
| API e2e smoke (`PlatformE2ETest`) | **PASS** (orchestrator run; see §3) |
| Contract drift | none |
| Blockers | none |

This stage generated and executed no API tests, launched no browser and called no endpoint, per the
API Tester rule for `API In Scope: NO`. Only this report and `summary.json` exist in this folder; there
is no `attempt-<n>/`, `results/junit.xml`, `discovery/` or `logs/` for this stage. The deferred e2e
regression was run afterwards by the orchestrator and is recorded in §3.

## 1. Specification evidence

`../specify/spec.md`, Change Scope Declaration (lines 50–51):

> | API In Scope | `NO`. No endpoint added, removed or changed. Two existing controllers move package; their paths, security and responses are unchanged (SPEC-022). |
> | API Impact Type | `NO_API_CHANGE` |

`../specify/spec.md`, API change assessment (lines 148–149):

> | API Impact Type | `NO_API_CHANGE` |
> | Endpoints added or changed | None. `TemporalAdminController` (`/api/recovery/v1/admin/...`) and `PlatformInfoController` (`/api/recovery/v1/platform/info`) change Java package only; paths, method security, request and response bodies are unchanged (SPEC-022 (e)). |

Machine-readable contracts agree: `../specify/contracts/backend-apis.json` has
`"apiInScope": false`, `"apiImpactType": "NO_API_CHANGE"`, `"endpoints": []`, and lists the two
controllers only under `relocatedEndpoints` with `"contractChange": "none"`.
`../plan/contracts/backend-apis.json` repeats this with `"endpointsAdded": []`,
`"endpointsChanged": []`.

## 2. Independent verification from the diff

Compared base `8675a5c` (merge-base of `HEAD` and `develop-recovery`) to `90550d3`
(`feature/RWB-TE-001-module-boundary`, 12 commits): **230 files, +3665 / −170**.

| Check | Command | Result |
|---|---|---|
| API specification file unchanged | `git diff --quiet 8675a5c..HEAD -- api/recovery-api-v4.yaml` | exit `0` (identical, 288,289 bytes) |
| Generated client types unchanged | `git diff --name-only 8675a5c..HEAD -- frontend/src/api/schema.d.ts` | no output |
| Production controllers | `git ls-tree` / file scan, `backend/src/main` | exactly 2 before and after; both pure renames |
| New production controllers or routes | `git diff --unified=0 -- backend/src/main`, filter `@RestController|@Controller|@RequestMapping|@FeignClient|@ResponseBody` | **0** added lines |
| Mapping / security / binding annotations anywhere | `git diff -M 8675a5c..HEAD --unified=0`, filter `@RequestMapping|@GetMapping|@PostMapping|@PutMapping|@PatchMapping|@DeleteMapping|@PreAuthorize|@ResponseStatus|@RequestBody|@PathVariable|@RequestParam` | **2** added lines, both in the new test-scope `access/internal/SecurityConfigTest.java` (nested `@WebMvcTest` `ProbeController`: `@GetMapping("/api/recovery/v1/test/probe")`, `@PreAuthorize("hasAuthority('RW-PLATADM')")`). Not an application endpoint and not packaged. |
| Added main classes | added paths under `backend/src/main` (66) | 61 `package-info.java` + 5 properties/configuration classes; no controller, no DTO |

Controller-by-controller (rename similarity from `git diff -M`):

| Controller | Move (base → head) | Similarity | Changed hunks | Path / security / bodies |
|---|---|---|---|---|
| `TemporalAdminController` | `recovery.workflow.internal` → `recovery.casewf.admin` | R093 | package line + imports only | Unchanged: `@RequestMapping("/api/recovery/v1/admin")`, `@GetMapping("/temporal/health")` + `@PreAuthorize("hasAnyAuthority('RW-PLATADM', 'RW-AUDIT')")`, `@PostMapping("/workflows/smoke")` + `@PreAuthorize("hasAuthority('RW-PLATADM')")`, records `SmokeStarted(workflowId, workflowType)`, `TemporalHealth`, `QueueHealth` |
| `PlatformInfoController` | `recovery.platform.internal` → `recovery.integration.internal` | R077 | package, imports, injected properties type, added `@EnableConfigurationProperties` registration | Unchanged: `@RequestMapping("/api/recovery/v1/platform")`, `@GetMapping("/info")`, `@PreAuthorize("isAuthenticated()")`, records `PlatformInfo(service, environment, flags, database)`, `DatabaseView(schema, recoveryTables, aceViews, visiblePublicTables)` |

Supporting classes on the response path only change package:

| File | Move | Similarity | Contract effect |
|---|---|---|---|
| `ApiError` | `recovery.platform.api` → `recovery.access.api` | R098 | none (package line only) |
| `ApiProblemException` | `recovery.platform.api` → `recovery.access.api` | R092 | none (package line only) |
| `ProblemFactory` | `recovery.platform.internal` → `recovery.access.internal` | R094 | none (package + import) |
| `ApiExceptionHandler` | `recovery.platform.internal` → `recovery.access.internal` | R091 | none (package + imports) |
| `SecurityConfig` | `recovery.platform.internal` → `recovery.access.internal` | R091 | none: same `/api/recovery/**` rules, open `/actuator/health`, 401 `MSG-P4-001` / 403 `MSG-P4-002` problem bodies, same CORS key `rwb.security.cors-origins`; only the properties bean changed (`RecoveryProperties.Security` → `RecoverySecurityProperties`, prefix `rwb.security`, same keys and defaults) |

API Specification v4 still defines the only specified endpoint on either controller as
`POST /admin/workflows/smoke` with `x-module: P3`, `x-capability` area "Platform administration" /
right `C`, `202` body `{workflowId, workflowType}`, plus `401`/`403`/`404`/`503`
(`api/recovery-api-v4.yaml` lines 3102–3133). `/platform/info` and `/admin/temporal/health` remain
local operational endpoints outside the specification, as the spec states. No drift.

**Conclusion: the spec's `NO_API_CHANGE` declaration is correct. No API change was missed.**

## 3. API e2e smoke — `PlatformE2ETest`

`backend/src/test/java/th/co/scb/ace/demo/e2e/PlatformE2ETest.java`, `@Tag("e2e")`, unchanged by
this branch (`git diff --stat 8675a5c..HEAD -- <file>` → empty). It is the regression guard for the
two relocated controllers: 6 REST Assured cases — `noTokenIsRefusedWithMsgP4001`,
`signedInPersonWithNoWorkbenchRoleIsRefusedWithMsgP4001`, `platformInfoShowsTheAdr010Boundary`,
`temporalHealthReportsNamespaceAndPlatformWorker`, `platformSmokeWorkflowStarts`,
`smokeNeedsPlatformAdminRight`.

| Item | Value |
|---|---|
| Status | **PASS** |
| Run by | Orchestrator, after this stage's N/A report; not re-run by the API Tester |
| Command | `backend> ./gradlew --no-daemon e2eTest` (worktree `RWB-TE-001`, against the local stack with the worktree backend) |
| Result | exit code `0`, `BUILD SUCCESSFUL in 52s`; `PlatformE2ETest` 6 tests, 0 failures, 0 errors, 0 skipped (JUnit XML `time="19.817"`) |
| Evidence | `../implement/backend/e2e.log` (Gradle output), `../implement/backend/e2e-backend.log` (worktree backend `bootRun` on :8080), `../implement/orchestrator-verify.md` run 5, `backend/build/test-results/e2eTest/TEST-th.co.scb.ace.demo.e2e.PlatformE2ETest.xml` in the worktree |
| Base URL / env | `RWB_E2E_BASE_URL` (default `http://localhost:8080`), `RWB_E2E_OIDC_URL` (default `http://localhost:8090/entra`) |
| Prerequisite | `scripts/dev.ps1 up -App` (backend, Postgres, Temporal, mock Entra ID); recorded in the orchestrator verification |

The pass closes the regression coverage for both relocated controllers: authentication (401
`MSG-P4-001`), role refusal, `/platform/info` ADR-010 boundary values, `/admin/temporal/health`,
`/admin/workflows/smoke`, and the `RW-PLATADM` right on the smoke endpoint.

## 4. Traceability and artifacts

- APT IDs: **none** (zero APIs in scope). No `Traceability_Matrix.md` rows are due from this stage;
  shared files were not edited.
- Written: `report.md`, `summary.json` (this folder).
- Not written: `api-inventory.json`, `api-test-cases.json`, `execution.json`, `results/junit.xml`,
  `logs/attempt.log`, `discovery/` — an N/A run creates none of these.

## 5. Status

```
API_TEST_STATUS: NOT_APPLICABLE [RUN_ID: INC-002-epic-1-RWB-TE-001] [APIS: 0] [CONTROLLERS: 0] [CASES: 0]
API_E2E_SMOKE: PASS [PlatformE2ETest 6 tests, 0 failures, exit 0, BUILD SUCCESSFUL in 52s; orchestrator run]
API_COVERAGE: [none]
CONTRACT_DRIFT: [none]
TEST_LOCATION: [not created: no API tests generated]
ARTIFACTS: [aisdlc/output/INC-002-epic-1-RWB-TE-001/api-tests/]
BLOCKERS: [none]
```

NEXT_STEP: Human review of API test results, then manually start Functional Automation Test with RUN_ID=INC-002-epic-1-RWB-TE-001
