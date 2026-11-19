# Recovery Workbench, local end-to-end workbench

A runnable local copy of the Recovery Workbench stack from document set v14: the recovery module of
ACE (ADR-001), its database boundary (ADR-010), Temporal (ADR-011), embedded Drools (ADR-012), the
Blob document hub (ADR-007) and Entra ID sign-in, all on one laptop.

The layout mirrors the ACE monorepo, so module code moves across unchanged:

| Here | In ACE |
|---|---|
| `backend/src/main/java/th/co/scb/ace/demo/recovery/` | same package |
| `backend/src/main/resources/db/modulemigration/recovery/` | same folder |
| `frontend/src/modules/recovery/` | same folder (ADR-006) |
| `frontend/src/{components/ui,lib,contexts,api}` | local stand-ins for the ACE shell entry points that D-RCV-39 allows |

## Layout

```
api/                       API Specification v4 (source of the generated frontend types)
backend/                   Spring Boot 4.1, Java 21, Gradle Kotlin DSL
  recovery/                Spring Modulith module "recovery"; one package per design module, each
                           with api/ (published) and internal/ (RWB-TE-001 module map)
    dataengine/            P1 data engine
    integration/           P2 integration: feature flags, platform info, outbound adapters
    casewf/                P3 case and workflow: config/ (parameter catalog, RWB-E1-042), migration/
                           (Flyway runner and lint, RWB-E1-044), rules/ (embedded Drools),
                           workflow/ (Temporal), timers/ (Quartz)
    access/                P4 access: security, capability checks, Problem errors
    dochub/                document hub: Azure Blob DocumentStore, write-once legal container
    agent/ ... writeoff/   empty module packages reserved for later epics
frontend/                  React 19, Vite 8, TypeScript, TanStack Query, i18next (th default), Tailwind
infra/
  postgres/init/           roles, databases and the ADR-010 grants
  postgres/schema/         ACE schema v1, Tier 2 probe, recovery Physical Schema v6 (copies from the set)
  temporal/                dynamic config, namespace search attributes
  mock-oidc/               local Entra ID stand-in, one client per Workbench role
scripts/dev.ps1            one entry point for every local command
docker-compose.yml         the local estate
```

## Prerequisites

Docker Desktop, JDK 21, Node 22. Gradle comes with the wrapper.

## Run it

```powershell
./scripts/dev.ps1 up          # Postgres, Temporal + UI, Azurite, mock Entra ID (creates .env on first run)
./scripts/dev.ps1 backend     # Spring Boot on :8080, profile local
./scripts/dev.ps1 frontend    # Vite on :5173
```

Or everything in containers: `./scripts/dev.ps1 up -App`.

| Service | Address |
|---|---|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8080 (`/api/recovery/v1`, `/actuator/health`) |
| Temporal UI | http://localhost:8233 (namespace `rwb-recovery`) |
| Postgres | localhost:5433, database `ace` |
| Mock Entra ID | http://localhost:8090/entra/.well-known/openid-configuration |
| Azurite Blob | http://localhost:10000/devstoreaccount1 |

The first `up` builds the database from the v14 sources and takes a minute or two.

### Signing in locally

The mock Entra ID shows a form. Enter any user name and, in **claims**, the roles to test:

```json
{ "aud": ["api://rwb-recovery"], "roles": ["RW-PLATADM"] }
```

For API calls, get a token per role with the client credentials grant. The client ID picks the
persona: `rwb-local-platadm`, `rwb-local-audit`, `rwb-local-coe`, `rwb-local-risk` or
`rwb-local-norole`.

```powershell
$t = (Invoke-RestMethod -Method Post http://localhost:8090/entra/token -Body @{grant_type="client_credentials"; client_id="rwb-local-platadm"; client_secret="x"; scope="api://rwb-recovery/.default"}).access_token
Invoke-RestMethod http://localhost:8080/api/recovery/v1/platform/info -Headers @{Authorization="Bearer $t"}
```

## Tests

| Command | What runs | Gate |
|---|---|---|
| `./scripts/dev.ps1 test` | Backend unit tests (Modulith boundaries, BND-5/6, workflow determinism, migration lint, Drools, codec, Temporal replay) and frontend typecheck, lint (D-RCV-39 import rule), Vitest with 80% coverage | Merge |
| `./scripts/dev.ps1 it` | `recoveryIntegrationTest`: builds the real database in Testcontainers and checks the ADR-010 grants, the recovery Flyway bean, the append-only decision log and the Temporal/ACE identity split. Fails, not skips, without Docker | Before any MR that touches a migration (D-RCV-44) |
| `./scripts/dev.ps1 e2e` | API e2e (REST Assured) and browser e2e (Playwright with an axe scan) against the running stack | SIT |

Coverage verification (`./gradlew recoveryCoverageVerification`) fails the build below 80% on four
counters: line, branch, instruction and method (RWB-TE-001). The CI job `backend-unit` runs it.

## Local versus target

| Concern | Local | SIT / UAT / PROD |
|---|---|---|
| ACE `public` schema | `ACE Schema PostgreSQL v1.sql` loaded at init | ACE team's database |
| Tier 2 ACE tables (RWB-ACE-001) | Probe DDL, `RWB_ACE_TIER2_PROBE=true` | ACE team's migration |
| Recovery schema | Physical Schema v6 loaded at init (`RWB_LOAD_REFERENCE_SCHEMA=true`) | Flyway migrations in story merge order (V0001 is RWB-E1-042; RWB-E1-001 adds the core tables later) |
| Temporal | `temporalio/auto-setup` on the shared Postgres, plaintext | Official Helm chart on ACE AKS, mTLS |
| Temporal client | Java SDK wired in `TemporalConfig` | ADR-011 names the Spring Boot starter; see below |
| Identity | mock-oauth2-server | Entra ID tenant with MFA |
| Blob | Azurite with a conditional write for legal documents | Azure Blob with an immutability policy, managed identity |
| Quartz / Batch | In memory | ACE JDBC job store |
| Secrets | `.env` (git-ignored, throwaway values) | Key Vault |

Keep `RWB_LOAD_REFERENCE_SCHEMA=true` until RWB-E1-001 delivers the core recovery tables as migrations.
Until then Flyway applies the story migrations on top of the reference schema, and the platform e2e
expects the reference tables. After RWB-E1-001, set `RWB_LOAD_REFERENCE_SCHEMA=false`, run
`./scripts/dev.ps1 reset` and then `up`; Flyway then builds the schema from
`db/modulemigration/recovery/`.

## Decisions taken while setting this up

These are local choices or conflicts found in the documents. Each one needs an owner's confirmation:

1. **Error body.** API Specification v4 returns RFC 7807 `Problem` (`messageCode`, `messageTh`,
   `traceId`) as `application/problem+json`. Backend standard BS-3.3 and frontend-context §6 say
   `{ code, messageId, message, fieldErrors, traceId }`. This build follows the specification,
   because it is the contract the frontend types are generated from. BS-3.3 should be aligned.
2. **Spring Boot 4.1.2, not 4.2.0-M2.** backend-context says ACE is on 4.2.0-M2. Spring Initializr
   offers 4.1.2 GA and 4.2.0-RC2. 4.1.2 is used here so that Drools and Temporal run on a GA
   baseline. Moving to 4.2 is a one-line change in `build.gradle.kts`.
3. **No Spring Cloud Azure, no Temporal Spring Boot starter.** Neither supports Boot 4.1 yet. The
   Azure Blob SDK and the Temporal SDK are wired directly, each in a single class.
4. **No Spring Modulith insight starter.** It proxies beans in `api` packages and cannot proxy
   records. Tracing still comes from Micrometer and OpenTelemetry.
5. **Platform messages in code.** MSG-P4-001/002/003 and MSG-P3-036 (English and Thai, from the
   Error and Message Standard v4) are held in `ApiError` because the message table is not seeded in
   Physical Schema v6. Story messages come from the message table.
6. **Operational endpoints outside the specification.** `GET /platform/info` and
   `GET /admin/temporal/health` are local operational endpoints (backend-context §3 and §7).
   `POST /admin/workflows/smoke` follows the specification exactly.
7. **Dictionary counts.** Physical Schema v6 seeds 123 `sys_objects` and 1,379 `sys_fields`;
   backend-context §4.2 says 122 and 1,366.

## Next

Pull stories in Build Sequence v6 order. Each story adds its migration as
`V<seq>__<story>_<name>.sql`, its code inside one nested module, and its screens under
`frontend/src/modules/recovery/`. The lint, boundary and coverage gates above apply from the first
file.
