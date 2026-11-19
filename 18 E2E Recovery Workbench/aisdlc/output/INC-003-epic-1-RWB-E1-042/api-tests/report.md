# API Test Report: RWB-E1-042 (parameter catalog)

RUN_ID INC-003-epic-1-RWB-E1-042. Stage: API Tester. This report records test results only. It records no approval (D-RUN-09).

> Provenance: the API Tester's own write of this file was blocked by the harness, so the orchestrator
> (Claude Code) saved the report text the agent returned, unchanged except for this note. Every figure
> below can be re-checked in `evidence/apiTest-run4.log` and `evidence/run4-junit/`.

API_TEST_STATUS: PASSED [APIS: 4] [CONTROLLERS: 1] [CASES: 13]

Code under test: worktree rwb-wt/RWB-E1-042, branch feature/RWB-E1-042-parameter-catalog, final tip 25c8f94 (the merged tip; tracked files unchanged by this stage).
Evidence: run5 (current), evidence/apiTest-run5.log, EXITCODE=0, 151 s, 13 tests, 13 passed, 0 failed, 0 errors, 0 skipped. Run5 JUnit XML was not kept; the counts come from the Gradle log. JUnit XML is kept for run4 at 9056ed2 (evidence/run4-junit/, same 13 cases; 9056ed2 to 25c8f94 changed tests and one comment only).
The contract test lives only in this folder and runs through an init script; moving it into backend/src/test is OPEN-057.
Runtime: Spring Boot test context with MockMvc, the real security filter chain, method checks and ApiExceptionHandler, against a Testcontainers postgres:16.16-alpine built from infra/postgres/init and schema. scripts/dev.ps1 up was not used and no base URL was called.
Build wiring: api-contract-init.gradle, an init script that adds an external apiTest source set and task. It does not change the repository or its build script.
Command (from backend/): `$env:JAVA_TOOL_OPTIONS="-Djdk.net.unixdomain.tmpdir=$env:USERPROFILE\.gradle\uds"; .\gradlew.bat --init-script "<repo>\aisdlc\output\INC-003-epic-1-RWB-E1-042\api-tests\api-contract-init.gradle" apiTest --rerun-tasks`
Prerequisites: Docker and Java 21. No secret environment variables are needed.

## Runs

| Run | Tip | Result | Status |
|---|---|---|---|
| run1 | 74e4ccb | earlier draft | Superseded |
| run2 | 74e4ccb | 10 cases, exit 0 | Superseded: the tip moved (CODE-001) and run2 had no load or repeat cases |
| run3 | 9056ed2 | exit 1, 12 passed, 1 failed | Superseded. Test setup fault: a nested class started a third Spring context and Postgres ran out of connection slots, so the context did not load. Not an application defect. |
| run4 | 9056ed2 | exit 0, 13/13 passed | Superseded: tip moved by test and comment changes only |
| run5 | 25c8f94 | exit 0, 13/13 passed (`ParameterApiContractIT` 12 + `$FlagOff` 1, 0 failed, 0 errors, 0 skipped), 151 s; `evidence/apiTest-run5.log` | Current |

parameter-config-it*.log are builder rechecks, not API Tester evidence.

## Inventory (base path /api/recovery/v1, API Specification v4)

| API ID | Endpoint | Controller or handler | Result |
|---|---|---|---|
| GETPARAM | GET /admin/parameters | ParameterCatalogController#list | PASSED |
| LOAD | POST /admin/reference-loads (PARAMETER), endpoint owned by RWB-E1-043 | ParameterLoadHandler#load | PASSED (interface) |
| APPROVE | POST /admin/reference-loads/{loadId}/approve, endpoint owned by RWB-E1-043 | ParameterLoadHandler#approve | PASSED (interface) |
| FLAGOFF | rwb.p3.configservice=false | controller absent; test-only stand-in for the RWB-E1-043 branch | PASSED |

## Cases (expected = actual, all PASSED)

| Case | Expected |
|---|---|
| APT-GETPARAM-001 | 200 with the v4 Parameter fields for case.entry.dpd in PROD |
| APT-GETPARAM-002 | 401 MSG-P4-001, with no token and with a token that has no RW- role |
| APT-GETPARAM-003 | 403 MSG-P4-002 with the "read parameters" action text, for RW-PHONECOL |
| APT-GETPARAM-004 | 422 MSG-GEN-002 field=environment |
| APT-GETPARAM-005 | a secret row is listed without value, default, version or validFrom |
| APT-GETPARAM-006 (new) | 503 status-only Problem (urn:rwb:problem:unavailable, no messageCode, no detail, no driver text) |
| APT-LOAD-001 | 422 MSG-P1-002 for a value over 400 characters; nothing written |
| APT-LOAD-002 (new) | new load: PARAMETER, validFrom, VALIDATED, rows=1, repeat=false. Identical repeat: same loadId, repeat=true, nothing written |
| APT-LOAD-003 (new) | identical repeat of an APPROVED load: same loadId, repeat=true, status APPROVED, no new rows; not 409 (CODE-001) |
| APT-APPROVE-001 | 409 MSG-GEN-004 on a repeated approval |
| APT-APPROVE-002 | 409 MSG-P3-027 for conflicting content at an approved valid-from; nothing written |
| APT-APPROVE-003 | 503 MSG-P7-003 when the recorder fails; rows stay VALIDATED with no approver |
| APT-FLAGOFF-001 | handler absent, GET 404, PARAMETER branch 404 MSG-P4-003 |

## Contract differences

1. GET /admin/parameters answers 422 MSG-GEN-002 for an environment outside the four, but API v4 lists only 200, 401, 403 and 503 and `environment` has no enum. Candidate document gap (the builder's DG-E042-ENV-422), Blocker No: v4 E422 already defines MSG-GEN-002, so only the operation's response list and the enum are missing; accepting any string would reopen SEC-042-01.
2. The response to an identical repeat load is not stated in API v4. The spec decides 201 with the existing load. Open as OI-E1-042-011, Blocker No.

## Not covered

- HTTP rendering, multipart parsing and C/A/U checks of reference-loads: RWB-E1-043 owns the endpoint.
- Rollback, MSG-P7-002, unknown loadId, MSG-GEN-002 range, MSG-GEN-001: left to the builder's ParameterConfigIT and ParameterLoadHandlerTest, to avoid duplicate cases.
- kind and owner filters: covered by ParameterCatalogControllerTest.
- Concurrent loads (TC-33): timing-dependent; covered by the builder's IT.
- Playwright and the MCP probe: no running backend (dev.ps1 up is forbidden) and no load endpoint.
- Traceability_Matrix: shared file; the orchestrator applies the APT rows.

BLOCKERS: none.
