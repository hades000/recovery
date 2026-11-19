# Phase 0 audit: the platform baseline against the AISDLC standards

- Run: 2026-11-17, about 23:05 to 23:09 +07:00.
- Agent: Explore subagent, read-only.
- Scope: commit `751909e` checked against `AGENTS.md`, the files in `aisdlc/.github/contexts/` and `aisdlc/.github/rules/`, and ADR-001 to ADR-012.
- Not re-reported: the deviations already recorded in `README.md` under "Decisions taken while setting this up" (items 1 to 7).

Each finding is carried to the story that owns it. Where no story in this delivery owns a finding, it is resolved by an `AISDLC-HARDENING` change, or recorded as out of scope and named in the final report.

## High

| # | Standard | Where | Gap | Owner |
|---|---|---|---|---|
| A-01 | BS-1.1, BS-1.3; module codes in the retirement registers (`recovery.casewf`, `recovery.accessadmin`, `recovery.dochub`, `recovery.integration`); `x-module` in API Spec v4 | `backend/.../recovery/{platform,rules,workflow,documents}` | Nested modules are technical slices. Nothing maps them to the P1–P10 / S1–S9 design modules. | RWB-TE-001 |
| A-02 | BS-1.3/1.4, backend-context §2 | `backend/src/test/resources/architecture/` (empty), `RecoveryBoundaryTest.java` | There is no module map. Only BND-5, BND-6 and the Temporal determinism check are tested. BND-1, BND-2 and BND-4 are missing, and so are the common/collection stubs. The BND-6 regex misses unqualified names and misses `PlatformInfoController`'s read of `information_schema` for `public`. | RWB-TE-001; BND-6 hardening in RWB-E1-069 |
| A-03 | BS-3.2, AGENTS §3.3, §3.2/§4.8 | `PlatformInfoController`, `TemporalAdminController`, `SecurityConfig` | Method checks name roles, or just `isAuthenticated()`, instead of the capability area and operation (`x-capability`). Role literals are in code. No test proves that every endpoint has a method check. | RWB-TE-003 (contract lint). The permission matrix is RWB-E1-037, outside this delivery. |
| A-04 | — | `RecoveryFlywayConfig`, `RecoveryMigrationLintTest`, `BlobDocumentStore`, `api:generate` | Parts of RWB-E1-044, RWB-TE-012 and RWB-TE-003 already exist in the baseline. Specs must treat them as baseline and must not duplicate them. | RWB-E1-044, RWB-TE-012, RWB-TE-003 |
| A-05 | AGENTS §5; v2 CLAUDE.md | `AGENTS.md` | The context paths in §5 do not resolve from the repository root; they live in `aisdlc/`. There is no package-level `AGENTS.md` and no coding-standard file. | RWB-TE-002 (repository governance) |

## Medium

| # | Standard | Where | Gap | Owner |
|---|---|---|---|---|
| A-06 | AGENTS §3.2/§4.8, backend-context §4.3, ADR-008 | `application.yaml`, `RecoveryFlags`, `@ConditionalOnProperty` | Flags and parameters are configuration literals, not reference data. There is no flag registry or owner. | RWB-E1-042 / RWB-E1-043 (parameters). The flag table is RWB-E1-047, outside this delivery. |
| A-07 | backend-context §7, BS-4.6 | `ApiExceptionHandler` | Raw exception text is logged, so SQL values can leak into logs. There is no correlation ID in the MDC, and `X-Correlation-Id` is neither read nor echoed. | RWB-TE-011 |
| A-08 | API Spec v4 Problem | `ProblemFactory`, `ApiExceptionHandler` | A generic 500 has no `messageCode` and no `traceId`. There is no 400 validation handler, so `field` is never set. `NOT_PERMITTED` fills `{action}` with English text, including in `messageTh`. | RWB-TE-003 |
| A-09 | testing-standards §1/§4, AGENTS §9 | `.gitlab-ci.yml` | CI has 3 jobs. The contract, PDPA lint, dependency scan, ZAP, Playwright/axe and coverage verification jobs are missing. | RWB-TE-003, RWB-TE-011 |
| A-10 | AGENTS §8, backend-context §2, OPEN-038 | repository root | There is no CODEOWNERS file and no MR template. | RWB-TE-002 |
| A-11 | FS-4.2, FS-1.2 | `frontend/src/modules/recovery/api/platform.ts`, `eslint.config.js` | Response types are written by hand. No fixture test proves that the import rule fires. | RWB-TE-003 |
| A-12 | `aisdlc/.github/rules/architectural-standards.md` | — | This file is a generic toolkit template: Flutter, `AUTH-XXX`, `/api/v1`. It conflicts with the project contexts and needs a tailoring note. | Orchestrator: tailoring note, document gap |
| A-13 | AGENTS §2, ADR-RCV-001 | `backend/build.gradle.kts` | Spring Session, Data REST and HATEOAS are absent, and no deviation is recorded for them. | Document gap. They are added only when a story needs them. |

## Low

| # | Gap | Owner |
|---|---|---|
| A-14 | No context records the versions of Vite, TS, Drools, the Temporal SDK and server, Modulith or Gradle (CTX-BE-GAP-04). The JaCoCo tool version is not pinned. ADR-RCV-001 still cites API Spec v2. | Orchestrator / document gap |
| A-15 | `QueryState.tsx` has no 401 or expired-session state (FS-3.1). | RWB-TE-003 or hardening |
| A-16 | `PlatformStatusPage.tsx` renders the flag keys as literal text (FS-2.3). | Hardening |
| A-17 | Nothing pins `rwb.schema` to `recovery` (D-RCV-28). | RWB-E1-044 |
| A-18 | The admin smoke endpoint writes no access-log entry (BS-4.4). That log is RWB-E1-039, outside this delivery. | Out of scope, recorded |
| A-19 | There are no story or plan files next to the code yet. Expected: the first story sets the convention. | RWB-E1-044 |

## Conforming

- `/api/recovery/v1` base path.
- Flyway settings (BS-2.3).
- Migration lint.
- Testcontainers PG 16 under `@Tag("recovery-it")`, which fails without Docker.
- Separate `e2eTest` task.
- `ModulithTest.verify()`.
- Frontend 80% thresholds.
- Thai-default i18n.
- D-RCV-39 import allow-list.
