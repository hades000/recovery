# Integration and API contract evidence: RWB-TE-001

## API impact

`NO_API_CHANGE` (spec.md "API change assessment"; `../specify/contracts/backend-apis.json`
`apiInScope: false`, `apiImpactType: NO_API_CHANGE`).

| Endpoint | Before | After | Contract change |
|---|---|---|---|
| `GET /api/recovery/v1/platform/info` | `platform.internal.PlatformInfoController` | `integration.internal.PlatformInfoController` | none: path, method security (`isAuthenticated()`), response record and counts unchanged |
| `GET /api/recovery/v1/admin/temporal/health` | `workflow.internal.TemporalAdminController` | `casewf.admin.TemporalAdminController` | none |
| `POST /api/recovery/v1/admin/workflows/smoke` | `workflow.internal.TemporalAdminController` | `casewf.admin.TemporalAdminController` | none; workflow ID, type, queue and 202 unchanged |

No OpenAPI file changed: `api/recovery-api-v4.yaml` is untouched (`git diff --name-only 8675a5c..HEAD`
has no `api/` path). `frontend/src/api/schema.d.ts` is untouched.

## Property contract

Keys, defaults and prefixes are unchanged (SPEC-023). The four records bind the same
`application.yaml` keys; the five T-TE001-12 binding tests pass on an isolated environment and in the
`.env`-importing `dev.ps1 test` run (TASK-17 Run 3, five methods PASS).

## Migration

None. No file under `backend/src/main/resources/db/**` changed; `RecoveryMigrationLintTest` passes
(3 tests).

## Functional test scenarios

| ID | Owner | Result |
|---|---|---|
| FTS-01 `/platform/info` unchanged | API Tester | `BLOCKED` — e2e needs the local stack (`deviations.md` DEV-01); controller moved package only; the MVC slice and `PlatformInfoControllerTest` cover the handler |
| FTS-02 `/admin/temporal/health`, `/admin/workflows/smoke` unchanged | API Tester | `BLOCKED` — same as FTS-01; `TemporalAdminControllerTest` covers both handlers and the 503 path |
| FTS-03 recovery Flyway still migrates the empty schema | Implementation Builder | `PASS` — `./gradlew recoveryIntegrationTest` exit 0, `RecoveryDatabaseIT` 6/6 (`backend/it.log`) |
| FTS-04 UI journeys | Functional Automation Test | `NOT_APPLICABLE` — UI In Scope NO |

## Evidence

- `backend/it.log` — Testcontainers run (`RecoveryDatabaseIT`, tag `recovery-it`).
- `backend/task17-run3.log` — merge-gate run with `.env` imported; the five binding methods PASS.
- `backend/coverage/recoveryCoverageReport.xml` — JaCoCo report over the relocated main classes.
